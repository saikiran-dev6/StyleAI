import io


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"StyleAI" in response.data
    assert b"Analyze My Style" in response.data
    assert b"How" in response.data and b"Works" in response.data
    assert b"About" in response.data



def test_analyze_route_no_face_error(client, monkeypatch):
    from styleai.routes import image_analyzer
    from styleai.services.image_analyzer import FaceNotFoundError

    def raise_no_face(path):
        raise FaceNotFoundError("No face detected in photo.")

    monkeypatch.setattr(image_analyzer, "analyze_image", raise_no_face)

    data = {
        "image": (io.BytesIO(b"fake image"), "test.jpg"),
        "gender": "Female"
    }
    response = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    res_data = response.get_json()
    assert res_data["success"] is False
    assert "No face detected" in res_data["error"]



def test_analyze_route_success(client, monkeypatch):
    from styleai.routes import image_analyzer

    mock_analysis = {
        "skin_tone": "Medium",
        "median_rgb": [170, 135, 115],
        "hex_color": "#aa8773",
        "luminance": 142.5,
        "confidence": 0.88,
        "face_box": {"x": 10, "y": 10, "w": 100, "h": 100}
    }
    monkeypatch.setattr(image_analyzer, "analyze_image", lambda path: mock_analysis)

    data = {
        "image": (io.BytesIO(b"fake image content"), "photo.jpg"),
        "gender": "Male"
    }
    response = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    res = response.get_json()
    assert res["success"] is True
    assert res["gender"] == "Male"
    assert res["analysis"]["skin_tone"] == "Medium"
    assert "recommendation" in res
    assert "shopping_links" in res


def test_analyze_route_invalid_gender_defaults_to_female(client, monkeypatch):
    from styleai.routes import image_analyzer

    mock_analysis = {
        "skin_tone": "Fair",
        "median_rgb": [220, 180, 160],
        "hex_color": "#dcb4a0",
        "luminance": 185.0,
        "confidence": 0.90,
        "face_box": {"x": 5, "y": 5, "w": 50, "h": 50}
    }
    monkeypatch.setattr(image_analyzer, "analyze_image", lambda path: mock_analysis)

    data = {
        "image": (io.BytesIO(b"fake image content"), "photo.jpg"),
        "gender": "InvalidGenderOption"
    }
    response = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    res = response.get_json()
    assert res["gender"] == "Female"


def test_analyze_route_empty_filename(client):
    data = {
        "image": (io.BytesIO(b"fake content"), ""),
        "gender": "Female"
    }
    response = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    res = response.get_json()
    assert res["success"] is False
    assert "No selected image file." in res["error"]


def test_analyze_route_image_analysis_error(client, monkeypatch):
    from styleai.routes import image_analyzer
    from styleai.services.image_analyzer import ImageAnalysisError

    def raise_analysis_error(path):
        raise ImageAnalysisError("Corrupt pixel data")

    monkeypatch.setattr(image_analyzer, "analyze_image", raise_analysis_error)

    data = {
        "image": (io.BytesIO(b"fake content"), "corrupt.jpg")
    }
    response = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    res = response.get_json()
    assert res["success"] is False
    assert "Corrupt pixel data" in res["error"]


def test_analyze_route_unexpected_exception(client, monkeypatch):
    from styleai.routes import image_analyzer

    def raise_runtime_error(path):
        raise RuntimeError("Unexpected error")

    monkeypatch.setattr(image_analyzer, "analyze_image", raise_runtime_error)

    data = {
        "image": (io.BytesIO(b"fake content"), "test.jpg")
    }
    response = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert response.status_code == 500
    res = response.get_json()
    assert res["success"] is False
    assert "Failed to analyze image" in res["error"]




