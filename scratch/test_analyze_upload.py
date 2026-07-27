import io
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from PIL import Image
from styleai import create_app

app = create_app()

img = Image.new("RGB", (600, 600), color=(210, 160, 140))
img_bytes = io.BytesIO()
img.save(img_bytes, format="JPEG")
img_bytes.seek(0)

with app.test_client() as client:
    res = client.post("/analyze", data={
        "image": (img_bytes, "test_face.jpg"),
        "gender": "Female"
    }, content_type="multipart/form-data")
    
    print("Status Code:", res.status_code)
    print("Response JSON keys:", list(res.get_json().keys()))
    print("Success:", res.get_json().get("success"))
    print("Analysis:", res.get_json().get("analysis"))
    print("Recommendation keys:", list(res.get_json().get("recommendation", {}).keys()))
    print("Shopping Links count:", len(res.get_json().get("shopping_links", [])))
