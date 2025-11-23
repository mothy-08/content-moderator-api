from fastapi.testclient import TestClient
from api.app import app, get_moderator
from api.content_moderator import ContentModerator


def mock_classifier(text):
    if text == "Hello":
        return [{"label": "safe", "score": 0.99}]
    return [{"label": "unsafe", "score": 0.99}]


def get_mock_moderator():
    return ContentModerator(classifier=mock_classifier)


app.dependency_overrides[get_moderator] = get_mock_moderator

client = TestClient(app)


def test_health():
    """Ensure the app is alive"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid_text():
    """Test the happy path with the mock."""
    response = client.post("/predict", json={"text": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "safe"
    assert data["score"] == 0.99
    assert data["confidence_text"] == "high"


def test_predict_normalization():
    """
    CRITICAL TEST: Verify that full-width characters are normalized.
    We send 'Ｈｅｌｌｏ' (Full width).
    If your normalization logic works, the classifier sees 'Hello' and returns 'clean'.
    If it fails, the classifier sees 'Ｈｅｌｌｏ' (unknown) and returns 'toxic' (default fallback in our mock).
    """
    response = client.post("/predict", json={"text": "Ｈｅｌｌｏ"})
    assert response.status_code == 200
    assert response.json()["label"] == "safe"


def test_predit_empty_text():
    """
    Test the Pydantic Bouncer
    Should fail with 422 Unprocessable Entity, NOT 500 Server Error
    """

    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422


def test_predict_whitespace_only():
    """
    Test Pydantic stripping whitespace.
    '   ' becomes '' -> min_length=1 fails.
    """
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 422
