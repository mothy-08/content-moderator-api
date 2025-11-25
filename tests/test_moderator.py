from fastapi.testclient import TestClient
from api.app import app, get_moderator
from api.content_moderator import ContentModerator


def mock_classifier(text):
    if text == "Hello":
        return [{"label": "SAFE", "score": 0.99}]
    return [{"label": "UNSAFE", "score": 0.99}]


def get_mock_moderator():
    return ContentModerator(mock_classifier)


app.dependency_overrides[get_moderator] = get_mock_moderator
client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid_text():
    response = client.post("/predict", json={"text": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "SAFE"
    assert data["score"] == 0.99


def test_predict_normalization():
    response = client.post("/predict", json={"text": "Ｈｅｌｌｏ"})
    assert response.status_code == 200
    assert response.json()["label"] == "SAFE"


def test_predict_empty_text():
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422


def test_predict_whitespace_only():
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 422
