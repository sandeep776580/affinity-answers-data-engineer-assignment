
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


def extract_products(
    html: str,
    base_url: str = BASE_URL,
) -> list[dict[str, str]]:
    """Extract product details from current and legacy product cards."""
    soup = BeautifulSoup(html, "html.parser")
    products = []
    seen_urls = set()

    links = soup.select(
        "a.product-image-link[href*='/product/'], "
        ".product-layout h4 a, "
        ".product-thumb h4 a, "
        ".product-card h4 a, "
        "a[href*='product_id=']"
    )

    for link in links:
        href = link.get("href", "").strip()
        product_url = urljoin(base_url, href)

        image = link.find("img")
        name = (
            image.get("alt", "").strip()
            if image and image.get("alt", "").strip()
            else " ".join(link.get_text(" ", strip=True).split())
        )

        # Find the closest ancestor containing the product price.
        card = link
        for _ in range(8):
            if card.parent is None:
                break
            card = card.parent
            if card.select_one(".price"):
                break

        # Legacy pages may put the title in a separate heading link.
        if not name:
            title_link = card.select_one(
                ".product-title a, h2 a, h3 a, h4 a"
            )
            if title_link:
                name = title_link.get_text(" ", strip=True)

        if not href or not name or product_url in seen_urls:
            continue

        price_node = card.select_one(".price")
        price = (
            " ".join(price_node.get_text(" ", strip=True).split())
            if price_node
            else ""
        )

        description_node = card.select_one(
            ".product-description, .description"
        )
        description = (
            " ".join(description_node.get_text(" ", strip=True).split())
            if description_node
            else ""
        )

        products.append({
            "name": name,
            "price": price,
            "description": description,
            "url": product_url,
        })
        seen_urls.add(product_url)

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
            headers={
                "User-Agent": "AffinityAnswersAssignmentScraper/1.0",
                "Accept": "text/html",
            },
            timeout=(10, 25),
        )
        response.raise_for_status()

    except requests.RequestException as exc:
        print(json.dumps({
            "search_term": search_term,
            "source_url": url,
            "error": str(exc),
        }, indent=2), file=sys.stderr)
        return 1

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ", strip=True).lower()

    if "attention required" in page_text and "cloudflare" in page_text:
        print(json.dumps({
            "search_term": search_term,
            "source_url": response.url,
            "error": "An access-restriction page was detected.",
            "product_count": 0,
            "products": [],
        }, indent=2))
        return 1

    products = extract_products(response.text, response.url)

    print(json.dumps({
        "search_term": search_term,
        "source_url": response.url,
        "product_count": len(products),
        "products": products,
        "note": (
            "No matching product cards were found in the returned HTML."
            if not products
            else ""
        ),
    }, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
