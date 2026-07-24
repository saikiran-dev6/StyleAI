import json
from typing import Any, Dict

from styleai.services.prompt_builder import build_fallback_recommendations


class RecommendationParser:
    @staticmethod
    def parse_and_validate(raw_text: str, gender: str, default_skin_tone: str) -> Dict[str, Any]:
        """
        Parses JSON string from Groq API and validates the required response schema.
        Falls back gracefully if response is malformed.
        """
        try:
            # Strip markdown codeblocks if LLM included them
            clean_text = raw_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()

            data = json.loads(clean_text)

            # Validate required root keys
            required_keys = ["skin_tone", "palette", "outfits", "hairstyle", "accessories", "rationale", "shopping_queries"]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required key in Groq response: {key}")

            # Enforce fallbacks for missing sub-keys
            if "confidence" not in data:
                data["confidence"] = 0.86

            palette = data.get("palette", {})
            for sub_key in ["primary", "secondary", "accent", "avoid"]:
                if sub_key not in palette or not isinstance(palette[sub_key], list):
                    palette[sub_key] = ["classic navy", "charcoal"] if sub_key != "avoid" else ["neon yellow"]
            data["palette"] = palette

            outfits = data.get("outfits", {})
            for sub_key in ["formal", "business", "casual", "party"]:
                if sub_key not in outfits or not isinstance(outfits[sub_key], list):
                    outfits[sub_key] = ["Tailored jacket", "Classic shirt"]
            data["outfits"] = outfits

            queries = data.get("shopping_queries", {})
            for ret in ["amazon_in", "myntra", "zara"]:
                if ret not in queries or not isinstance(queries[ret], list):
                    queries[ret] = [f"{gender} formal shirt", f"{gender} casual jacket"]
            data["shopping_queries"] = queries

            return data

        except Exception:
            return build_fallback_recommendations(gender=gender, skin_tone=default_skin_tone)
