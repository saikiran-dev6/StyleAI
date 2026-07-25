import io

import pytest

from styleai.services.image_analyzer import FaceNotFoundError, ImageAnalysisError, ImageAnalyzer


def test_image_analyzer_no_face(dummy_non_face_image_bytes):
    analyzer = ImageAnalyzer()
    buf = io.BytesIO(dummy_non_face_image_bytes)
    res = analyzer.analyze_image(buf)
    assert res["skin_tone"] in ["Fair", "Medium", "Olive", "Deep"]



def test_image_analyzer_invalid_file():
    analyzer = ImageAnalyzer()
    buf = io.BytesIO(b"not an image stream")
    with pytest.raises(ImageAnalysisError):
        analyzer.analyze_image(buf)


def test_image_analyzer_success_with_mocked_face(monkeypatch):
    from unittest.mock import MagicMock

    import numpy as np
    from PIL import Image

    img = Image.new("RGB", (400, 400), color=(210, 165, 145))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    analyzer = ImageAnalyzer()
    mock_cascade = MagicMock()
    mock_cascade.empty.return_value = False
    mock_cascade.detectMultiScale.return_value = np.array([[50, 50, 200, 200]])
    monkeypatch.setattr(analyzer, "face_cascade", mock_cascade)

    res = analyzer.analyze_image(buf)
    assert res["skin_tone"] in ["Fair", "Medium", "Olive", "Deep"]
    assert "hex_color" in res
    assert res["confidence"] > 0
    assert res["face_box"] == {"x": 50, "y": 50, "w": 200, "h": 200}



def test_image_analyzer_large_image_resizing(monkeypatch):
    from unittest.mock import MagicMock

    import numpy as np
    from PIL import Image

    img = Image.new("RGB", (1600, 1600), color=(220, 180, 160))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    analyzer = ImageAnalyzer()
    mock_cascade = MagicMock()
    mock_cascade.detectMultiScale.return_value = np.array([[100, 100, 400, 400]])
    monkeypatch.setattr(analyzer, "face_cascade", mock_cascade)

    res = analyzer.analyze_image(buf)
    assert res["skin_tone"] in ["Fair", "Medium", "Olive", "Deep"]


def test_image_analyzer_fallback_center_roi(monkeypatch):
    from unittest.mock import MagicMock

    import numpy as np
    from PIL import Image

    # Dark background and black face region so HSV filtering on subregions returns empty mask
    img = Image.new("RGB", (400, 400), color=(5, 5, 5))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    analyzer = ImageAnalyzer()
    mock_cascade = MagicMock()
    mock_cascade.detectMultiScale.return_value = np.array([[50, 50, 200, 200]])
    monkeypatch.setattr(analyzer, "face_cascade", mock_cascade)

    res = analyzer.analyze_image(buf)
    assert "skin_tone" in res



def test_haarcascade_path_and_cascade_init_fallbacks(monkeypatch):
    import os

    from styleai.services.image_analyzer import get_haarcascade_path

    monkeypatch.setattr(os.path, "exists", lambda p: "alt_path" in str(p) or "haarcascade_frontalface_default.xml" in str(p))
    path = get_haarcascade_path()
    assert "haarcascade" in path

    # Test complete fallback when no file exists
    monkeypatch.setattr(os.path, "exists", lambda p: False)
    assert get_haarcascade_path() == "haarcascade_frontalface_default.xml"


