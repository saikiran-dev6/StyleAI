import io
import os

from werkzeug.datastructures import FileStorage

from styleai.utils.file_utils import delete_temp_file, save_temp_file


def test_save_and_delete_temp_file():
    fs = FileStorage(
        stream=io.BytesIO(b"dummy image content"),
        filename="test_upload.png",
        content_type="image/png"
    )

    saved_path = save_temp_file(fs, target_dir="/tmp/styleai_tests_file_utils")
    assert os.path.exists(saved_path)

    delete_temp_file(saved_path)
    assert not os.path.exists(saved_path)


def test_delete_non_existent_file():
    # Should not raise exception
    delete_temp_file("/tmp/styleai_tests_non_existent.png")


def test_delete_temp_file_oserror(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda p: True)

    def raise_oserror(p):
        raise OSError("Permission denied")

    monkeypatch.setattr(os, "remove", raise_oserror)
    # Should catch OSError silently without raising
    delete_temp_file("/tmp/dummy_path.png")


