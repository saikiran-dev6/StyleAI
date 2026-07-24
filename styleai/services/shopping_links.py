from abc import ABC, abstractmethod
from typing import Any, Dict, List
from urllib.parse import quote_plus


class ShoppingLinkProvider(ABC):
    @abstractmethod
    def generate_search_url(self, query: str) -> str:
        pass


class AmazonIndiaProvider(ShoppingLinkProvider):
    def generate_search_url(self, query: str) -> str:
        encoded = quote_plus(query)
        return f"https://www.amazon.in/s?k={encoded}"


class MyntraProvider(ShoppingLinkProvider):
    def generate_search_url(self, query: str) -> str:
        encoded = quote_plus(query)
        return f"https://www.myntra.com/{encoded}"


class ZaraProvider(ShoppingLinkProvider):
    def generate_search_url(self, query: str) -> str:
        encoded = quote_plus(query)
        return f"https://www.zara.com/in/en/search?searchTerm={encoded}"


class ShoppingLinkService:
    def __init__(self):
        self.providers: Dict[str, ShoppingLinkProvider] = {
            "amazon_in": AmazonIndiaProvider(),
            "myntra": MyntraProvider(),
            "zara": ZaraProvider()
        }

    def build_retailer_links(self, shopping_queries: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Generates product link items with title, retailer name, search URL, and display tag.
        """
        results = []
        retailer_display_names = {
            "amazon_in": "Amazon India",
            "myntra": "Myntra",
            "zara": "Zara"
        }

        for key, queries in shopping_queries.items():
            provider = self.providers.get(key)
            if not provider or not isinstance(queries, list):
                continue

            retailer_name = retailer_display_names.get(key, key.upper())
            for q in queries:
                url = provider.generate_search_url(q)
                results.append({
                    "title": q.title(),
                    "retailer": retailer_name,
                    "retailer_key": key,
                    "url": url,
                    "query": q
                })

        return results
