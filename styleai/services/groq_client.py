import logging
from typing import Any, Dict, List

from openai import OpenAI

from styleai.config import Config
from styleai.services.prompt_builder import (
    build_fallback_recommendations,
    build_system_prompt,
    build_user_prompt,
)
from styleai.services.recommendation_parser import RecommendationParser

logger = logging.getLogger("styleai")


class GroqClient:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.base_url = Config.GROQ_BASE_URL
        self.model = Config.GROQ_MODEL
        self.timeout = Config.GROQ_TIMEOUT_SECONDS
        self.max_tokens = Config.GROQ_MAX_OUTPUT_TOKENS
        self.temperature = Config.GROQ_TEMPERATURE

    def get_style_recommendation(self, gender: str, skin_tone: str, median_rgb: List[int]) -> Dict[str, Any]:
        """
        Sends skin tone stats to Groq LLaMA 3.3 70B and parses response JSON object.
        Falls back safely to fallback template if Groq API key is missing or call fails.
        """
        if not self.api_key or self.api_key.startswith("gsk_your_groq_api_key"):
            logger.warning("GROQ_API_KEY not configured or placeholder detected. Operating in mock fallback mode.")
            return build_fallback_recommendations(gender=gender, skin_tone=skin_tone)

        try:
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout
            )

            system_prompt = build_system_prompt()
            user_prompt = build_user_prompt(gender=gender, skin_tone=skin_tone, median_rgb=median_rgb)

            logger.info(f"Calling Groq API model {self.model} for gender={gender}, skin_tone={skin_tone}")
            response = client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            content = response.choices[0].message.content
            return RecommendationParser.parse_and_validate(content, gender=gender, default_skin_tone=skin_tone)

        except Exception as e:
            logger.error(f"Groq API call failed: {str(e)}. Using fallback recommendations.")
            return build_fallback_recommendations(gender=gender, skin_tone=skin_tone)
