"""
Pytest configuration and shared fixtures.

This file is automatically loaded by pytest and provides reusable
test fixtures for all test files.
"""

import pytest
from app import app as flask_app


@pytest.fixture
def app():
    """
    Provides a Flask application configured for testing.

    Usage in tests:
        def test_something(app):
            assert app.config['TESTING'] is True
    """
    flask_app.config.update({
        'TESTING': True,
        'OPENWEATHER_API_KEY': 'test_api_key_12345',
    })

    yield flask_app

    # Cleanup after test (if needed)
    # Reset any global state here


@pytest.fixture
def client(app):
    """
    Provides a test client for making HTTP requests to the Flask app.

    Usage in tests:
        def test_route(client):
            response = client.get('/')
            assert response.status_code == 200
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Provides a CLI test runner for testing Flask CLI commands.

    Usage in tests:
        def test_cli_command(runner):
            result = runner.invoke(cli_command)
            assert result.exit_code == 0
    """
    return app.test_cli_runner()


# Mock API Response Fixtures

@pytest.fixture
def mock_weather_success():
    """
    Mock successful OpenWeather API response for current weather.

    Returns a dictionary matching the OpenWeather API structure.
    """
    return {
        "name": "Melbourne",
        "main": {
            "temp": 22.5,
            "feels_like": 21.8,
            "humidity": 65
        },
        "weather": [
            {
                "description": "clear sky",
                "icon": "01d"
            }
        ],
        "wind": {
            "speed": 3.5
        }
    }


@pytest.fixture
def mock_forecast_success():
    """
    Mock successful OpenWeather API response for 5-day forecast.

    Returns a dictionary matching the OpenWeather forecast API structure.
    """
    return {
        "list": [
            {
                "dt_txt": "2025-10-23 12:00:00",
                "main": {"temp": 22.5},
                "weather": [{"icon": "01d"}]
            },
            {
                "dt_txt": "2025-10-23 15:00:00",
                "main": {"temp": 24.0},
                "weather": [{"icon": "01d"}]
            },
            {
                "dt_txt": "2025-10-24 12:00:00",
                "main": {"temp": 20.0},
                "weather": [{"icon": "02d"}]
            },
            {
                "dt_txt": "2025-10-24 15:00:00",
                "main": {"temp": 21.5},
                "weather": [{"icon": "02d"}]
            },
            {
                "dt_txt": "2025-10-25 12:00:00",
                "main": {"temp": 19.0},
                "weather": [{"icon": "03d"}]
            },
        ]
    }


@pytest.fixture
def mock_weather_api_error():
    """
    Mock OpenWeather API error response.

    Used to test error handling when API is unavailable.
    """
    return {
        "cod": "500",
        "message": "Internal server error"
    }
