import logging

from flask import Blueprint, jsonify, render_template, request

from styleai.services.groq_client import GroqClient
from styleai.services.image_analyzer import FaceNotFoundError, ImageAnalysisError, ImageAnalyzer
from styleai.services.shopping_links import ShoppingLinkService
from styleai.utils.file_utils import delete_temp_file, save_temp_file
from styleai.utils.security import is_allowed_file, sanitize_filename

bp = Blueprint("routes", __name__)
logger = logging.getLogger("styleai")

image_analyzer = ImageAnalyzer()
groq_client = GroqClient()
shopping_service = ShoppingLinkService()


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided in request."}), 400

    file = request.files["image"]
    gender = request.form.get("gender", "Female").capitalize()

    if gender not in ["Male", "Female"]:
        gender = "Female"

    if file.filename == "":
        return jsonify({"success": False, "error": "No selected image file."}), 400

    cleaned_filename = sanitize_filename(file.filename)
    if not is_allowed_file(cleaned_filename, file.content_type):
        return jsonify({
            "success": False,
            "error": "Invalid file format. Allowed formats: PNG, JPG, JPEG, GIF, WEBP."
        }), 400

    temp_path = None
    try:
        temp_path = save_temp_file(file)
        analysis = image_analyzer.analyze_image(temp_path)

        recommendation = groq_client.get_style_recommendation(
            gender=gender,
            skin_tone=analysis["skin_tone"],
            median_rgb=analysis["median_rgb"]
        )

        shopping_links = shopping_service.build_retailer_links(
            recommendation.get("shopping_queries", {})
        )

        return jsonify({
            "success": True,
            "gender": gender,
            "analysis": analysis,
            "recommendation": recommendation,
            "shopping_links": shopping_links
        })

    except FaceNotFoundError as e:
        logger.warning(f"Face detection failed: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400

    except ImageAnalysisError as e:
        logger.error(f"Image analysis error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400

    except Exception:
        logger.exception("Unexpected error in /analyze handler")
        return jsonify({"success": False, "error": "Failed to analyze image. Please try another clear photo."}), 500

    finally:
        if temp_path:
            delete_temp_file(temp_path)


@bp.route("/health", methods=["GET"])
@bp.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "running", "service": "styleai-web"}), 200



@bp.route("/readyz", methods=["GET"])
def readyz():
    return jsonify({"status": "ready", "service": "styleai-web"}), 200


@bp.route("/version", methods=["GET"])
def version():
    return jsonify({
        "version": "1.0.0",
        "app": "StyleAI",
        "model": "llama-3.3-70b-versatile"
    }), 200
