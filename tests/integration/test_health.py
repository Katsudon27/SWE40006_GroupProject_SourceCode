"""
Integration tests for the /health endpoint.

Tests health check functionality including uptime tracking
and last successful API fetch timestamp.
"""

import pytest


@pytest.mark.integration
def test_health_endpoint(client):
    """Test that /health endpoint returns correct status and fields."""
    # Arrange & Act
    response = client.get('/health')
    data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert 'status' in data
    assert data['status'] == 'ok'
    assert 'uptime_seconds' in data
    assert isinstance(data['uptime_seconds'], int)
    assert data['uptime_seconds'] >= 0
    assert 'last_successful_fetch' in data


@pytest.mark.integration
def test_health_endpoint_uptime_increases(client):
    """Test that uptime increases between successive calls."""
    import time

    # First call
    response1 = client.get('/health')
    uptime1 = response1.get_json()['uptime_seconds']

    # Wait a bit
    time.sleep(1)

    # Second call
    response2 = client.get('/health')
    uptime2 = response2.get_json()['uptime_seconds']

    # Uptime should have increased
    assert uptime2 >= uptime1