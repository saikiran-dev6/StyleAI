import io
from unittest.mock import patch


def test_smoke_local_pipeline_success(client, dummy_face_image_bytes):
    """
    Smoke tests full end-to-end request pipeline by mocking image_analyzer to return a successful face analysis
    so that route, Groq client, link builder, and JSON serialization run end-to-end.
    """
    mock_analysis = {
        "skin_tone": "Medium",
        "median_rgb": [172, 138, 120],
        "hex_color": "#ac8a78",
        "luminance": 143.5,
        "confidence": 0.88,
        "face_box": {"x": 100, "y": 100, "w": 150, "h": 150}
    }

    with patch("styleai.routes.image_analyzer.analyze_image", return_value=mock_analysis):
        data = {
            "image": (io.BytesIO(dummy_face_image_bytes), "test.jpg"),
            "gender": "Female"
        }
        response = client.post("/analyze", data=data, content_type="multipart/form-data")
        assert response.status_code == 200

        res = response.get_json()
        assert res["success"] is True
        assert res["gender"] == "Female"
        assert res["analysis"]["skin_tone"] == "Medium"
        assert "recommendation" in res
        assert "shopping_links" in res
        assert len(res["shopping_links"]) > 0
