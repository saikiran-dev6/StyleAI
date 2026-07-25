import os
from typing import Any, Dict

import cv2
import numpy as np
from PIL import Image, ImageOps

from styleai.utils.color_utils import (
    calculate_luminance,
    classify_skin_tone_from_luma_and_rgb,
    rgb_to_hex,
)


class ImageAnalysisError(Exception):
    pass


class FaceNotFoundError(ImageAnalysisError):
    pass


def get_haarcascade_path() -> str:
    # 1. Bundled local data directory (bulletproof across Vercel, Docker, Windows, Linux)
    bundled_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "haarcascade_frontalface_default.xml")
    if os.path.exists(bundled_path):
        return bundled_path

    # 2. Fall back to cv2 package data
    try:
        if hasattr(cv2, "data") and hasattr(cv2.data, "haarcascades"):
            path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
            if os.path.exists(path):
                return path
    except Exception:
        pass
    try:
        cv2_dir = os.path.dirname(cv2.__file__)
        alt_path = os.path.join(cv2_dir, "data", "haarcascade_frontalface_default.xml")
        if os.path.exists(alt_path):
            return alt_path
    except Exception:
        pass
    return "haarcascade_frontalface_default.xml"


class ImageAnalyzer:
    def __init__(self):
        self._face_cascade = None

    @property
    def face_cascade(self):
        if self._face_cascade is None:
            try:
                cascade_path = get_haarcascade_path()
                self._face_cascade = cv2.CascadeClassifier(cascade_path)
                if self._face_cascade.empty():
                    self._face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            except Exception:
                self._face_cascade = cv2.CascadeClassifier()
        return self._face_cascade

    @face_cascade.setter
    def face_cascade(self, value):
        self._face_cascade = value

    def analyze_image(self, file_path_or_bytes) -> Dict[str, Any]:
        """
        Loads image, detects face ROI, extracts skin RGB percentiles,
        computes luminance, and classifies skin tone into Fair, Medium, Olive, or Deep.
        """
        try:
            pil_img = Image.open(file_path_or_bytes)
            pil_img = ImageOps.exif_transpose(pil_img)
            pil_img = pil_img.convert("RGB")
        except Exception as e:
            raise ImageAnalysisError(f"Failed to load image file: {str(e)}")

        img_w, img_h = pil_img.width, pil_img.height

        # Proportional resize if longest edge exceeds 1280px
        max_dim = max(img_w, img_h)
        if max_dim > 1280:
            scale = 1280.0 / max_dim
            img_w = int(img_w * scale)
            img_h = int(img_h * scale)
            pil_img = pil_img.resize((img_w, img_h), Image.Resampling.LANCZOS)

        # Convert Pillow RGB -> OpenCV BGR
        rgb_np = np.array(pil_img)
        bgr_np = cv2.cvtColor(rgb_np, cv2.COLOR_RGB2BGR)

        # Face detection multi-tier attempt
        gray = cv2.cvtColor(bgr_np, cv2.COLOR_BGR2GRAY)
        faces = []
        try:
            if not self.face_cascade.empty():
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(80, 80)
                )
                if len(faces) == 0:
                    faces = self.face_cascade.detectMultiScale(
                        gray,
                        scaleFactor=1.05,
                        minNeighbors=3,
                        minSize=(40, 40)
                    )
        except Exception:
            faces = []

        is_fallback_center = False
        if len(faces) == 0:
            # Fallback to center 50% region of the uploaded image
            is_fallback_center = True
            fx = int(img_w * 0.25)
            fy = int(img_h * 0.20)
            fw = int(img_w * 0.50)
            fh = int(img_h * 0.50)
        else:
            # Select largest face box (w * h)
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            fx, fy, fw, fh = largest_face

        # ROI fractions relative to face box
        rois_spec = [
            # Left cheek: x 0.18w-0.38w, y 0.52h-0.72h
            (int(fx + 0.18 * fw), int(fy + 0.52 * fh), int(0.20 * fw), int(0.20 * fh)),
            # Right cheek: x 0.62w-0.82w, y 0.52h-0.72h
            (int(fx + 0.62 * fw), int(fy + 0.52 * fh), int(0.20 * fw), int(0.20 * fh)),
            # Forehead: x 0.30w-0.70w, y 0.18h-0.32h
            (int(fx + 0.30 * fw), int(fy + 0.18 * fh), int(0.40 * fw), int(0.14 * fh)),
        ]

        skin_pixels_rgb = []

        for rx, ry, rw, rh in rois_spec:
            if rw <= 0 or rh <= 0:
                continue
            roi_rgb = rgb_np[ry:ry + rh, rx:rx + rw]
            if roi_rgb.size == 0:
                continue

            roi_hsv = cv2.cvtColor(roi_rgb, cv2.COLOR_RGB2HSV)
            # Filter HSV: V < 45 or V > 245 (shadows/highlights), S < 10 (gray/noise)
            v = roi_hsv[:, :, 2]
            s = roi_hsv[:, :, 1]

            mask = (v >= 45) & (v <= 245) & (s >= 10)
            valid_rgb = roi_rgb[mask]
            if len(valid_rgb) > 0:
                skin_pixels_rgb.append(valid_rgb)

        if not skin_pixels_rgb:
            # Fallback to center face box if filtered subregions returned empty
            center_roi = rgb_np[int(fy + 0.2 * fh):int(fy + 0.8 * fh), int(fx + 0.2 * fw):int(fx + 0.8 * fw)]
            all_pixels = center_roi.reshape(-1, 3)
        else:
            all_pixels = np.vstack(skin_pixels_rgb)

        if len(all_pixels) == 0:
            # Full image fallback
            all_pixels = rgb_np.reshape(-1, 3)


        # NumPy 20th–80th percentile trimming per channel
        trimmed_rgb = []
        for ch in range(3):
            p20 = np.percentile(all_pixels[:, ch], 20)
            p80 = np.percentile(all_pixels[:, ch], 80)
            ch_data = all_pixels[:, ch]
            valid_mask = (ch_data >= p20) & (ch_data <= p80)
            trimmed_rgb.append(ch_data[valid_mask])

        # Calculate median RGB
        med_r = int(np.median(trimmed_rgb[0])) if len(trimmed_rgb[0]) > 0 else int(np.median(all_pixels[:, 0]))
        med_g = int(np.median(trimmed_rgb[1])) if len(trimmed_rgb[1]) > 0 else int(np.median(all_pixels[:, 1]))
        med_b = int(np.median(trimmed_rgb[2])) if len(trimmed_rgb[2]) > 0 else int(np.median(all_pixels[:, 2]))

        median_rgb = [med_r, med_g, med_b]
        luma = calculate_luminance((med_r, med_g, med_b))
        skin_tone = classify_skin_tone_from_luma_and_rgb(luma, (med_r, med_g, med_b))
        hex_color = rgb_to_hex((med_r, med_g, med_b))

        # Confidence calculation based on retained pixel sample count and bounds
        sample_count = len(all_pixels)
        confidence = min(0.98, max(0.70, round(0.75 + (sample_count / 10000.0) * 0.2, 2)))

        return {
            "skin_tone": skin_tone,
            "median_rgb": median_rgb,
            "hex_color": hex_color,
            "luminance": round(luma, 2),
            "confidence": confidence,
            "face_box": {"x": int(fx), "y": int(fy), "w": int(fw), "h": int(fh)}
        }
