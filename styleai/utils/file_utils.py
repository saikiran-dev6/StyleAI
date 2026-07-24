import os
import uuid

from styleai.config import Config


def save_temp_file(file_storage, target_dir: str = None) -> str:
    if target_dir is None:
        target_dir = Config.UPLOAD_TMP_DIR
    os.makedirs(target_dir, exist_ok=True)

    unique_prefix = uuid.uuid4().hex[:10]
    filename = f"{unique_prefix}_{file_storage.filename}"
    filepath = os.path.join(target_dir, filename)
    file_storage.save(filepath)
    return filepath


def delete_temp_file(filepath: str) -> None:
    if filepath and os.path.exists(filepath):
        try:
            os.remove(filepath)
        except OSError:
            pass
