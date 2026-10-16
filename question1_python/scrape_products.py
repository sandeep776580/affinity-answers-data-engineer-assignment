
"""Search MD Computers and output product information as JSON."""

import json
import sys
from urllib.parse import urlencode, urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mdcomputers.in/"


def build_search_url(search_term: str) -> str:
    """Build a search URL with safely encoded input."""
    query = urlencode({
        "route": "product/search",
        "search": search_term,
    })
    return f"{BASE_URL}?{query}"


def extract_products(html: str, base_url: str = BASE_URL) -> list[dict[str, str]]:
    """Extract product information from recognized product cards."""
    soup = BeautifulSoup(html, "html.parser")
    products = []
    seen = set()

    cards = soup.select(
        ".product-layout, .product-thumb, .product-card"
    )

    for card in cards:
        link = card.select_one(
            "h4 a, .caption h4 a, a[href*='product_id=']"
        )
        if not link:
            continue

        name = " ".join(link.get_text(" ", strip=True).split())
        href = link.get("href", "").strip()

        if not name or not href:
            continue

        product_url = urljoin(base_url, href)
        key = (name, product_url)

        if key in seen:
            continue

        price_node = card.select_one(".price")
        description_node = card.select_one(".description")

        price = (
            " ".join(price_node.get_text(" ", strip=True).split())
            if price_node else ""
        )
        description = (
            " ".join(description_node.get_text(" ", strip=True).split())
            if description_node else ""
        )

        products.append({
            "name": name,
            "price": price,
            "description": description,
            "url": product_url,
        })
        seen.add(key)

    return products


def main() -> int:
    search_term = input("Enter a product search term: ").strip()

    if not search_term:
        print("Error: search term cannot be empty.", file=sys.stderr)
        return 2

    url = build_search_url(search_term)

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=25,
        )

        if response.status_code == 403:
            print(json.dumps({
                "search_term": search_term,
                "source_url": url,
                "error": "HTTP 403: Access denied by the website.",
                "explanation": (
                    "The server returned an access-denied response, "
                    "so product extraction could not be performed."
                ),
                "next_step": (
                    "Check whether the page is accessible in a normal browser "
                    "or contact the website owner for authorized access."
                ),
                "product_count": 0,
                "products": [],
            }, indent=2))
            return 1

        response.raise_for_status()

    except requests.RequestException as exc:
        print(json.dumps({
            "search_term": search_term,
            "source_url": url,
            "error": str(exc),
        }, indent=2), file=sys.stderr)
        return 1

    products = extract_products(response.text, response.url)

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ", strip=True).lower()

    if "attention required" in page_text and "cloudflare" in page_text:
        print(json.dumps({
            "search_term": search_term,
            "source_url": response.url,
            "error": "An anti-bot or access-restriction page was detected.",
            "product_count": 0,
            "products": [],
        }, indent=2))
        return 1

    print(json.dumps({
        "search_term": search_term,
        "source_url": response.url,
        "product_count": len(products),
        "products": products,
        "note": (
            "No matching product cards were found in the returned HTML."
            if not products else ""
        ),
    }, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
