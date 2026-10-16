import unittest
from scrape_products import build_search_url, extract_products


class ScraperTests(unittest.TestCase):
    def test_search_term_is_encoded(self):
        url = build_search_url("external hard drives")
        self.assertIn("external+hard+drives", url)

    def test_extracts_product_card(self):
        html = """
        <div class="product-layout">
          <div class="product-thumb">
            <div class="caption">
              <h4><a href="https://example.test/item?product_id=7">Test SSD</a></h4>
              <p class="description">Fast storage</p>
              <div class="price">₹1,000</div>
            </div>
          </div>
        </div>
        """
        products = extract_products(html)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Test SSD")
        self.assertEqual(products[0]["price"], "₹1,000")


if __name__ == "__main__":
    unittest.main()
