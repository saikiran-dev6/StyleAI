import io

from styleai.utils.security import is_allowed_file, sanitize_filename


def test_filename_sanitization():
    assert sanitize_filename("../../malicious.exe") == "malicious.exe"
    assert sanitize_filename("my photo.jpg") == "my_photo.jpg"
    assert sanitize_filename("") == "upload.jpg"


def test_is_allowed_file():
    assert is_allowed_file("test.png", "image/png") is True
    assert is_allowed_file("photo.JPG", "image/jpeg") is True
    assert is_allowed_file("bad.exe", "application/x-msdownload") is False
    assert is_allowed_file("noextension", "image/png") is False
    assert is_allowed_file("test.png", "application/pdf") is False



def test_upload_missing_file(client):
    response = client.post("/analyze", data={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "No image file" in data["error"]


def test_upload_disallowed_extension(client):
    data = {
        "image": (io.BytesIO(b"fake script"), "test.txt")
    }
    response = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    res_data = response.get_json()
    assert res_data["success"] is False
    assert "Invalid file format" in res_data["error"]
