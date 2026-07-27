import os

from dotenv import load_dotenv

import tempfile

load_dotenv()


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    SECRET_KEY = os.getenv("SECRET_KEY", "styleai-secret-key-default-change-me")
    MAX_CONTENT_LENGTH_MB = int(os.getenv("MAX_CONTENT_LENGTH_MB", "10"))
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH_MB * 1024 * 1024
    UPLOAD_TMP_DIR = os.getenv("UPLOAD_TMP_DIR") or os.path.join(tempfile.gettempdir(), "styleai")

    # Groq configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("PI_KEY", "")
    GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_TIMEOUT_SECONDS = int(os.getenv("GROQ_TIMEOUT_SECONDS", "8"))
    GROQ_MAX_OUTPUT_TOKENS = int(os.getenv("GROQ_MAX_OUTPUT_TOKENS", "1200"))
    GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.7"))

    # Server binding
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", "8080"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Allowed Upload File Extensions & MIME types
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    ALLOWED_MIME_TYPES = {
        "image/png",
        "image/jpeg",
        "image/pjpeg",
        "image/gif",
        "image/webp"
    }

    # Skin Tone Luma Thresholds
    SKIN_TONE_THRESHOLDS = {
        "FAIR": 190,
        "MEDIUM_UPPER": 189,
        "MEDIUM_LOWER": 155,
        "OLIVE_UPPER": 154,
        "OLIVE_LOWER": 110,
        "DEEP": 110
    }
