from typing import Any, Dict, List


def build_system_prompt() -> str:
    return (
        "You are StyleAI, a JSON-only fashion recommendation engine. "
        "Return valid JSON and no prose outside JSON. "
        "Strictly produce fashion styling tailored to the provided gender, skin tone, and RGB characteristics."
    )


def build_user_prompt(gender: str, skin_tone: str, median_rgb: List[int]) -> str:
    return (
        f"Gender: {gender}. "
        f"Skin tone class: {skin_tone}. "
        f"Median RGB: {median_rgb}. "
        "Produce a structured styling guide formatted EXACTLY as a single JSON object with these exact keys: "
        "skin_tone, confidence, palette (primary, secondary, accent, avoid), outfits (formal, business, casual, party), "
        "hairstyle (recommendations, maintenance), accessories, rationale, shopping_queries (amazon_in, myntra, zara). "
        "Provide 2-3 search query phrases per retailer under shopping_queries."
    )


def build_fallback_recommendations(gender: str, skin_tone: str) -> Dict[str, Any]:
    """Fallback JSON payload if Groq API is unavailable or returns invalid format."""
    is_female = (gender.lower() == "female")

    if skin_tone == "Fair":
        palette = {
            "primary": ["emerald green", "navy blue", "royal ruby"],
            "secondary": ["soft cream", "heather gray", "rose dust"],
            "accent": ["rose gold", "sapphire"],
            "avoid": ["washed out beige", "stark neon yellow"]
        }
        rationale = "Rich jewel tones and contrasting deep shades complement fair skin tones without washing out natural luminescence."
    elif skin_tone == "Medium":
        palette = {
            "primary": ["teal", "navy", "burgundy"],
            "secondary": ["cream", "charcoal", "olive"],
            "accent": ["gold", "rust"],
            "avoid": ["neon yellow", "muddy gray"]
        }
        rationale = "Muted jewel tones complement the detected medium skin tone and maintain rich contrast without washing out the complexion."
    elif skin_tone == "Olive":
        palette = {
            "primary": ["burnt orange", "warm olive", "rich maroon"],
            "secondary": ["warm beige", "deep brown", "khaki"],
            "accent": ["warm gold", "bronze"],
            "avoid": ["cool pastels", "icy blue"]
        }
        rationale = "Earthy warm tones accentuate natural golden and green undertones, enhancing olive skin luminosity."
    else:  # Deep
        palette = {
            "primary": ["cobalt blue", "mustard yellow", "fuchsia"],
            "secondary": ["stark white", "crisp ivory", "deep plum"],
            "accent": ["bright gold", "silver"],
            "avoid": ["muddy brown", "dark gray"]
        }
        rationale = "Vibrant high-contrast hues and bold primaries bring out the natural glow and depth of deep skin tones."

    outfits = {
        "formal": [
            "Tailored blazer suit in " + palette["primary"][1],
            "Silk shirt in " + palette["secondary"][0],
            "Structured trousers in " + palette["secondary"][1]
        ],
        "business": [
            "Smart collar shirt in " + palette["secondary"][0],
            "Chinos/trousers in " + palette["primary"][0],
            "Leather loafers"
        ],
        "casual": [
            "Over-shirt in " + palette["primary"][0],
            "Classic dark denim jeans",
            "Minimalist white sneakers"
        ],
        "party": [
            "Statement jacket/dress in " + palette["primary"][2],
            "Accent accessories in " + palette["accent"][0]
        ]
    }

    hairstyle = {
        "recommendations": ["Soft textured waves", "Layered mid-length cut"] if is_female else ["Textured fade cut", "Classic side-part pompadour"],
        "maintenance": ["Use light hydrating serum", "Trim every 4 to 6 weeks"]
    }

    accessories = [
        f"{palette['accent'][0].title()} timepiece",
        "Minimalist chain necklace",
        "Structured leather bag"
    ]

    shopping_queries = {
        "amazon_in": [
            f"{gender} {palette['primary'][1]} blazer",
            f"{gender} {palette['accent'][0]} watch"
        ],
        "myntra": [
            f"{gender} {palette['primary'][2]} party dress" if is_female else f"{gender} {palette['primary'][2]} shirt",
            f"{gender} {palette['primary'][0]} casual jacket"
        ],
        "zara": [
            f"{gender} {palette['secondary'][0]} shirt",
            f"{gender} structured handbag" if is_female else f"{gender} leather shoes"
        ]
    }

    return {
        "skin_tone": skin_tone,
        "confidence": 0.88,
        "palette": palette,
        "outfits": outfits,
        "hairstyle": hairstyle,
        "accessories": accessories,
        "rationale": rationale,
        "shopping_queries": shopping_queries
    }
