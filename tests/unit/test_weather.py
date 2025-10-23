"""
Unit tests for the get_weather() function.

Tests weather data retrieval from OpenWeather API including
success cases, error handling, and edge cases.
"""

import pytest
import responses
from requests.exceptions import RequestException
from app import get_weather


@pytest.mark.unit
@responses.activate
def test_get_weather_success(mock_weather_success):
    """Test successful weather data retrieval for a valid city."""
    # Arrange
    city = "Melbourne"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/weather",
        json=mock_weather_success,
        status=200
    )

    # Act
    result = get_weather(city)

    # Assert
    assert result is not None
    assert result["name"] == "Melbourne"
    assert result["temp"] == 22.5
    assert result["feels_like"] == 21.8
    assert result["condition"] == "clear sky"
    assert result["icon"] == "01d"
    assert result["humidity"] == 65
    assert result["wind_speed"] == 3.5


@pytest.mark.unit
@responses.activate
def test_get_weather_invalid_city():
    """Test handling of invalid/non-existent city name."""
    # Arrange
    city = "NonExistentCity123"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/weather",
        json={"cod": "404", "message": "city not found"},
        status=404
    )

    # Act
    result = get_weather(city)

    # Assert
    assert result is None


@pytest.mark.unit
@responses.activate
def test_get_weather_api_server_error():
    """Test handling of API server errors (5xx)."""
    # Arrange
    city = "Melbourne"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/weather",
        json={"cod": "500", "message": "Internal server error"},
        status=500
    )

    # Act
    result = get_weather(city)

    # Assert
    assert result is None


@pytest.mark.unit
@responses.activate
def test_get_weather_network_error():
    """Test handling of network connection errors."""
    # Arrange
    city = "Melbourne"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/weather",
        body=RequestException("Connection timeout")
    )

    # Act
    result = get_weather(city)

    # Assert
    assert result is None


@pytest.mark.unit
@responses.activate
def test_get_weather_malformed_response():
    """Test handling of malformed API response (missing fields)."""
    # Arrange
    city = "Melbourne"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/weather",
        json={"name": "Melbourne"},  # Missing required fields
        status=200
    )

    # Act
    result = get_weather(city)

    # Assert
    assert result is None


@pytest.mark.unit
@responses.activate
def test_get_weather_different_cities():
    """Test weather retrieval for multiple different cities."""
    cities_data = [
        ("London", "overcast clouds", "04d", 15.0),
        ("Tokyo", "light rain", "10d", 18.5),
        ("Sydney", "partly cloudy", "02d", 25.0),
    ]

    for city, condition, icon, temp in cities_data:
        # Arrange
        responses.add(
            responses.GET,
            f"https://api.openweathermap.org/data/2.5/weather",
            json={
                "name": city,
                "main": {"temp": temp, "feels_like": temp - 1, "humidity": 70},
                "weather": [{"description": condition, "icon": icon}],
                "wind": {"speed": 5.0}
            },
            status=200
        )

        # Act
        result = get_weather(city)

        # Assert
        assert result is not None
        assert result["name"] == city
        assert result["temp"] == temp
        assert result["condition"] == condition
        assert result["icon"] == icon

        # Clear responses for next iteration
        responses.reset()


@pytest.mark.unit
@responses.activate
def test_get_weather_special_characters_in_city():
    """Test handling of city names with special characters."""
    # Arrange
    city = "São Paulo"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/weather",
        json={
            "name": "São Paulo",
            "main": {"temp": 28.0, "feels_like": 27.5, "humidity": 80},
            "weather": [{"description": "sunny", "icon": "01d"}],
            "wind": {"speed": 2.5}
        },
        status=200
    )

    # Act
    result = get_weather(city)

    # Assert
    assert result is not None
    assert result["name"] == "São Paulo"


@pytest.mark.unit
@responses.activate
def test_get_weather_extreme_temperatures():
    """Test handling of extreme temperature values."""
    # Arrange
    city = "Antarctica"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/weather",
        json={
            "name": "Antarctica",
            "main": {"temp": -50.0, "feels_like": -60.0, "humidity": 10},
            "weather": [{"description": "clear sky", "icon": "01d"}],
            "wind": {"speed": 30.0}
        },
        status=200
    )

    # Act
    result = get_weather(city)

    # Assert
    assert result is not None
    assert result["temp"] == -50.0
    assert result["feels_like"] == -60.0
