from werkzeug.utils import secure_filename

from styleai.config import Config


def sanitize_filename(filename: str) -> str:
    cleaned = secure_filename(filename)
    if not cleaned:
        cleaned = "upload.jpg"
    return cleaned


def is_allowed_file(filename: str, content_type: str = None) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    if ext not in Config.ALLOWED_EXTENSIONS:
        return False
    if content_type and content_type.lower() not in Config.ALLOWED_MIME_TYPES:
        return False
    return True
