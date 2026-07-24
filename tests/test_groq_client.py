from unittest.mock import MagicMock, patch

from styleai.services.groq_client import GroqClient
from styleai.services.recommendation_parser import RecommendationParser


def test_groq_client_mock_fallback():
    client = GroqClient()
    result = client.get_style_recommendation(gender="Female", skin_tone="Medium", median_rgb=[170, 135, 115])
    assert result["skin_tone"] == "Medium"
    assert "palette" in result
    assert "outfits" in result
    assert "shopping_queries" in result


def test_groq_client_with_api_key_mocked_success():
    client = GroqClient()
    client.api_key = "gsk_real_test_key_12345"

    mock_chat_completion = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = """
    {
        "skin_tone": "Medium",
        "confidence": 0.88,
        "palette": {
            "primary": ["teal"],
            "secondary": ["cream"],
            "accent": ["gold"],
            "avoid": ["yellow"]
        },
        "outfits": {
            "formal": ["teal dress"],
            "business": ["cream suit"],
            "casual": ["jeans"],
            "party": ["gold dress"]
        },
        "hairstyle": {"recommendations": ["waves"], "maintenance": ["trim"]},
        "accessories": ["earrings"],
        "rationale": "Teal complements medium skin tones perfectly.",
        "shopping_queries": {
            "amazon_in": ["teal dress"],
            "myntra": ["cream suit"],
            "zara": ["gold dress"]
        }
    }
    """
    mock_chat_completion.choices = [mock_choice]

    with patch("styleai.services.groq_client.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value = mock_chat_completion

        res = client.get_style_recommendation(gender="Female", skin_tone="Medium", median_rgb=[170, 135, 115])
        assert res["skin_tone"] == "Medium"
        assert res["rationale"] == "Teal complements medium skin tones perfectly."


def test_groq_client_api_exception_fallback():
    client = GroqClient()
    client.api_key = "gsk_real_test_key_12345"

    with patch("styleai.services.groq_client.OpenAI", side_effect=Exception("API connection timeout")):
        res = client.get_style_recommendation(gender="Female", skin_tone="Olive", median_rgb=[140, 130, 100])
        assert res["skin_tone"] == "Olive"
        assert "palette" in res


def test_recommendation_parser_valid_json():
    raw_json = """
    {
        "skin_tone": "Fair",
        "confidence": 0.90,
        "palette": {
            "primary": ["navy", "ruby"],
            "secondary": ["cream"],
            "accent": ["gold"],
            "avoid": ["yellow"]
        },
        "outfits": {
            "formal": ["navy suit"],
            "business": ["blue shirt"],
            "casual": ["white tee"],
            "party": ["red dress"]
        },
        "hairstyle": {
            "recommendations": ["waves"],
            "maintenance": ["serum"]
        },
        "accessories": ["watch"],
        "rationale": "High contrast works great.",
        "shopping_queries": {
            "amazon_in": ["navy suit women"],
            "myntra": ["red dress"],
            "zara": ["white tee"]
        }
    }
    """
    parsed = RecommendationParser.parse_and_validate(raw_json, gender="Female", default_skin_tone="Fair")
    assert parsed["skin_tone"] == "Fair"
    assert parsed["palette"]["primary"] == ["navy", "ruby"]
    assert parsed["shopping_queries"]["amazon_in"] == ["navy suit women"]


def test_recommendation_parser_fallback_on_corrupt():
    raw_json = "NOT VALID JSON"
    parsed = RecommendationParser.parse_and_validate(raw_json, gender="Male", default_skin_tone="Deep")
    assert parsed["skin_tone"] == "Deep"
    assert "outfits" in parsed


def test_recommendation_parser_markdown_codeblocks():
    raw_json = """```json
    {
        "skin_tone": "Fair",
        "palette": {"primary": ["navy"], "secondary": ["white"], "accent": ["gold"], "avoid": ["neon"]},
        "outfits": {"formal": ["suit"], "business": ["shirt"], "casual": ["tee"], "party": ["blazer"]},
        "hairstyle": {"recommendations": ["short"]},
        "accessories": ["ring"],
        "rationale": "Markdown test.",
        "shopping_queries": {"amazon_in": ["suit"], "myntra": ["shirt"], "zara": ["blazer"]}
    }
    ```"""
    parsed = RecommendationParser.parse_and_validate(raw_json, gender="Male", default_skin_tone="Fair")
    assert parsed["skin_tone"] == "Fair"
    assert parsed["confidence"] == 0.86


def test_recommendation_parser_missing_subkeys():
    raw_json = """
    {
        "skin_tone": "Medium",
        "palette": {},
        "outfits": {},
        "hairstyle": "bobs",
        "accessories": ["watch"],
        "rationale": "Incomplete subkeys test.",
        "shopping_queries": {}
    }
    """
    parsed = RecommendationParser.parse_and_validate(raw_json, gender="Female", default_skin_tone="Medium")
    assert parsed["skin_tone"] == "Medium"
    assert "primary" in parsed["palette"]
    assert "formal" in parsed["outfits"]
    assert "amazon_in" in parsed["shopping_queries"]


def test_recommendation_parser_missing_root_key():
    raw_json = """
    {
        "skin_tone": "Fair"
    }
    """
    parsed = RecommendationParser.parse_and_validate(raw_json, gender="Female", default_skin_tone="Fair")
    assert parsed["skin_tone"] == "Fair"
    assert "outfits" in parsed

