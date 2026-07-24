import io

import cv2
import numpy as np
import pytest
from PIL import Image

from styleai import create_app
from styleai.config import Config


class TestConfig(Config):
    TESTING = True
    FLASK_ENV = "testing"
    SECRET_KEY = "test-secret-key"
    UPLOAD_TMP_DIR = "/tmp/styleai_tests"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def dummy_face_image_bytes():
    """Generates a synthetic image with a skin-colored oval so OpenCV face/skin analyzer can sample it."""
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    # Background light gray
    img[:] = (220, 220, 220)
    # Draw face oval with realistic skin color (BGR)
    cv2.ellipse(img, (200, 200), (90, 120), 0, 0, 360, (140, 160, 210), -1)
    # Draw eyes
    cv2.circle(img, (165, 170), 12, (50, 50, 50), -1)
    cv2.circle(img, (235, 170), 12, (50, 50, 50), -1)
    # Mouth
    cv2.ellipse(img, (200, 250), (35, 15), 0, 0, 180, (80, 80, 180), 3)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.getvalue()


@pytest.fixture
def dummy_non_face_image_bytes():
    """Generates a blank image without any face."""
    pil_img = Image.new("RGB", (200, 200), color=(10, 10, 10))
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.getvalue()
