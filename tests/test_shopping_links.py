from styleai.services.shopping_links import ShoppingLinkService


def test_shopping_link_generation():
    service = ShoppingLinkService()
    queries = {
        "amazon_in": ["navy blazer", "gold watch"],
        "myntra": ["burgundy dress"],
        "zara": ["white shirt"]
    }
    links = service.build_retailer_links(queries)
    assert len(links) == 4

    amazon_links = [item for item in links if item["retailer_key"] == "amazon_in"]
    assert len(amazon_links) == 2
    assert "amazon.in" in amazon_links[0]["url"]
    assert "navy+blazer" in amazon_links[0]["url"] or "navy" in amazon_links[0]["url"]

    myntra_links = [item for item in links if item["retailer_key"] == "myntra"]
    assert "myntra.com" in myntra_links[0]["url"]

    zara_links = [item for item in links if item["retailer_key"] == "zara"]
    assert "zara.com" in zara_links[0]["url"]


def test_shopping_links_unknown_provider_and_invalid_queries():
    service = ShoppingLinkService()
    queries = {
        "unknown_store": ["some item"],
        "amazon_in": "not a list"
    }
    links = service.build_retailer_links(queries)
    assert len(links) == 0


