import pytest
from feedback.models import Feedback


@pytest.fixture
def feedback():
    return Feedback.objects.create(
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/500.00 (KHTML, like Gecko) Ubuntu Chromium/60.0.1234.56 Chrome/60.0.1234.56 Safari/500.00',
        rating=1,
        body='My feedback',
        url='https://example.com/service',
        email='john.smith@example.com',
    )


@pytest.mark.django_db
def test_feedback_model_creation(feedback):
    assert Feedback.objects.count() == 1


@pytest.mark.django_db
def test_posting_to_api_base(client):
    resp = client.post('/v1/')
    assert resp.status_code == 400
