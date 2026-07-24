

def test_413_error_handler(app):
    client = app.test_client()

    @app.route("/test-413")
    def trigger_413():
        from werkzeug.exceptions import RequestEntityTooLarge
        raise RequestEntityTooLarge()

    response = client.get("/test-413")
    assert response.status_code == 413
    data = response.get_json()
    assert data["success"] is False
    assert "File size exceeds maximum allowed limit" in data["error"]


def test_500_error_handler(app):
    client = app.test_client()

    @app.route("/test-500")
    def trigger_500():
        from werkzeug.exceptions import InternalServerError
        raise InternalServerError()

    response = client.get("/test-500")
    assert response.status_code == 500
    data = response.get_json()
    assert data["success"] is False
    assert "internal server error" in data["error"].lower()
