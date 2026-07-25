def test_healthz_endpoint(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "running"
    assert data["service"] == "styleai-web"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "running"



def test_readyz_endpoint(client):
    response = client.get("/readyz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ready"


def test_version_endpoint(client):
    response = client.get("/version")
    assert response.status_code == 200
    data = response.get_json()
    assert "version" in data
    assert data["app"] == "StyleAI"
