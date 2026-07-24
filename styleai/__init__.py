import os

from flask import Flask, jsonify

from styleai.config import Config
from styleai.logging_config import setup_logging


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
        static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    )

    app.config.from_object(config_class)

    try:
        from flask_cors import CORS
        CORS(app)
    except ImportError:
        pass

    # Ensure temporary upload directory exists
    os.makedirs(app.config["UPLOAD_TMP_DIR"], exist_ok=True)

    # Setup logger
    setup_logging()


    # Register routes
    from styleai.routes import bp
    app.register_blueprint(bp)

    # Security headers middleware
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' data: blob:; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "script-src 'self' 'unsafe-inline'; "
            "connect-src 'self';"
        )
        return response

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            "success": False,
            "error": f"File size exceeds maximum allowed limit of {Config.MAX_CONTENT_LENGTH_MB}MB."
        }), 413

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": "An internal server error occurred while processing your request."
        }), 500

    return app
