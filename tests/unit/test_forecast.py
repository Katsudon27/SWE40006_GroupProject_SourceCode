"""
Unit tests for the get_forecast() function.

Tests 5-day forecast data retrieval from OpenWeather API including
success cases, error handling, and data aggregation logic.
"""

import pytest
import responses
from requests.exceptions import RequestException
from app import get_forecast


@pytest.mark.unit
@responses.activate
def test_get_forecast_success(mock_forecast_success):
    """Test successful forecast retrieval for a valid city."""
    # Arrange
    city = "Melbourne"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json=mock_forecast_success,
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
    assert len(result) <= 5  # Should return max 5 days


@pytest.mark.unit
@responses.activate
def test_get_forecast_data_structure():
    """Test that forecast data has correct structure."""
    # Arrange
    city = "Sydney"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={
            "list": [
                {
                    "dt_txt": "2025-10-23 12:00:00",
                    "main": {"temp": 20.0},
                    "weather": [{"icon": "01d"}]
                },
                {
                    "dt_txt": "2025-10-23 15:00:00",
                    "main": {"temp": 22.0},
                    "weather": [{"icon": "01d"}]
                }
            ]
        },
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is not None
    assert len(result) == 1  # One day
    forecast_day = result[0]
    assert "date" in forecast_day
    assert "temp_min" in forecast_day
    assert "temp_max" in forecast_day
    assert "icon" in forecast_day


@pytest.mark.unit
@responses.activate
def test_get_forecast_temperature_aggregation():
    """Test that min/max temperatures are correctly calculated per day."""
    # Arrange
    city = "Tokyo"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={
            "list": [
                {"dt_txt": "2025-10-23 00:00:00", "main": {"temp": 15.0}, "weather": [{"icon": "01d"}]},
                {"dt_txt": "2025-10-23 06:00:00", "main": {"temp": 18.0}, "weather": [{"icon": "02d"}]},
                {"dt_txt": "2025-10-23 12:00:00", "main": {"temp": 25.0}, "weather": [{"icon": "01d"}]},
                {"dt_txt": "2025-10-23 18:00:00", "main": {"temp": 20.0}, "weather": [{"icon": "03d"}]},
            ]
        },
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is not None
    assert len(result) == 1
    assert result[0]["temp_min"] == 15.0
    assert result[0]["temp_max"] == 25.0
    assert result[0]["date"] == "2025-10-23"


@pytest.mark.unit
@responses.activate
def test_get_forecast_multiple_days():
    """Test forecast grouping across multiple days."""
    # Arrange
    city = "London"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={
            "list": [
                {"dt_txt": "2025-10-23 12:00:00", "main": {"temp": 20.0}, "weather": [{"icon": "01d"}]},
                {"dt_txt": "2025-10-24 12:00:00", "main": {"temp": 18.0}, "weather": [{"icon": "02d"}]},
                {"dt_txt": "2025-10-25 12:00:00", "main": {"temp": 22.0}, "weather": [{"icon": "01d"}]},
            ]
        },
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is not None
    assert len(result) == 3
    assert result[0]["date"] == "2025-10-23"
    assert result[1]["date"] == "2025-10-24"
    assert result[2]["date"] == "2025-10-25"


@pytest.mark.unit
@responses.activate
def test_get_forecast_limits_to_five_days():
    """Test that forecast returns maximum 5 days even if more data available."""
    # Arrange
    city = "Paris"
    forecast_data = {
        "list": [
            {"dt_txt": f"2025-10-{20+i} 12:00:00", "main": {"temp": 20.0}, "weather": [{"icon": "01d"}]}
            for i in range(10)  # 10 days of data
        ]
    }
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json=forecast_data,
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is not None
    assert len(result) == 5  # Should limit to 5 days


@pytest.mark.unit
@responses.activate
def test_get_forecast_invalid_city():
    """Test handling of invalid/non-existent city name."""
    # Arrange
    city = "NonExistentCity123"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={"cod": "404", "message": "city not found"},
        status=404
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is None


@pytest.mark.unit
@responses.activate
def test_get_forecast_api_server_error():
    """Test handling of API server errors (5xx)."""
    # Arrange
    city = "Berlin"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={"cod": "500", "message": "Internal server error"},
        status=500
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is None


@pytest.mark.unit
@responses.activate
def test_get_forecast_network_error():
    """Test handling of network connection errors."""
    # Arrange
    city = "Rome"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        body=RequestException("Connection timeout")
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is None


@pytest.mark.unit
@responses.activate
def test_get_forecast_malformed_response_no_list():
    """Test handling of malformed response (missing 'list' field)."""
    # Arrange
    city = "Madrid"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={"cod": "200"},  # Missing 'list' field
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is None


@pytest.mark.unit
@responses.activate
def test_get_forecast_malformed_response_missing_fields():
    """Test handling of entries with missing required fields."""
    # Arrange
    city = "Vienna"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={
            "list": [
                {"dt_txt": "2025-10-23 12:00:00", "main": {"temp": 20.0}},  # Missing 'weather'
            ]
        },
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is None


@pytest.mark.unit
@responses.activate
def test_get_forecast_empty_list():
    """Test handling of empty forecast list."""
    # Arrange
    city = "Athens"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={"list": []},
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 0


@pytest.mark.unit
@responses.activate
def test_get_forecast_extreme_temperatures():
    """Test handling of extreme temperature values."""
    # Arrange
    city = "Antarctica"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={
            "list": [
                {"dt_txt": "2025-10-23 12:00:00", "main": {"temp": -60.0}, "weather": [{"icon": "01d"}]},
                {"dt_txt": "2025-10-23 18:00:00", "main": {"temp": -45.0}, "weather": [{"icon": "01d"}]},
            ]
        },
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is not None
    assert len(result) == 1
    assert result[0]["temp_min"] == -60.0
    assert result[0]["temp_max"] == -45.0


@pytest.mark.unit
@responses.activate
def test_get_forecast_uses_first_icon_of_day():
    """Test that the first icon of each day is used."""
    # Arrange
    city = "Dublin"
    responses.add(
        responses.GET,
        f"https://api.openweathermap.org/data/2.5/forecast",
        json={
            "list": [
                {"dt_txt": "2025-10-23 06:00:00", "main": {"temp": 15.0}, "weather": [{"icon": "01d"}]},
                {"dt_txt": "2025-10-23 12:00:00", "main": {"temp": 20.0}, "weather": [{"icon": "02d"}]},
                {"dt_txt": "2025-10-23 18:00:00", "main": {"temp": 18.0}, "weather": [{"icon": "03d"}]},
            ]
        },
        status=200
    )

    # Act
    result = get_forecast(city)

    # Assert
    assert result is not None
    assert len(result) == 1
    assert result[0]["icon"] == "01d"  # Should be first icon
