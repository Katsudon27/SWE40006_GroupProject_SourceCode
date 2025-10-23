import pytest
import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_health_endpoint(client):
    # Ensure the /health endpoint returns expected keys
    rv = client.get('/health')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'status' in data
    assert data['status'] == 'ok'
    assert 'uptime_seconds' in data
    assert isinstance(data['uptime_seconds'], int)
    assert 'last_successful_fetch' in data