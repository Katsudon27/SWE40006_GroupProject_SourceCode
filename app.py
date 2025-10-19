from flask import Flask, render_template, request, redirect, url_for
import requests
import logging
import time
import os
from dotenv import load_dotenv

# This loads variables from .env into environment
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

app_start_time = time.time()
last_successful_fetch = None

def update_last_successful_fetch():
    global last_successful_fetch
    last_successful_fetch = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        update_last_successful_fetch()
        return {
            "name": data["name"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "condition": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        update_last_successful_fetch()
        # Group by day, get high/low and icon for each day
        forecast = []
        days = {}
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            temp = entry["main"]["temp"]
            icon = entry["weather"][0]["icon"]
            if date not in days:
                days[date] = {"temps": [], "icons": []}
            days[date]["temps"].append(temp)
            days[date]["icons"].append(icon)
        for date, info in list(days.items())[:5]:
            forecast.append({
                "date": date,
                "temp_min": min(info["temps"]),
                "temp_max": max(info["temps"]),
                "icon": info["icons"][0]
            })
        return forecast
    except requests.RequestException as e:
        logging.error(f"Forecast API request failed: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather = get_weather(city)
            forecast = get_forecast(city)
            if not weather or not forecast:
                error = "Could not fetch weather data. Please check the city name or try again later."
        else:
            error = "Please enter a city name."
    return render_template("index.html", weather=weather, forecast=forecast, error=error)

@app.route("/health")
def health():
    uptime = int(time.time() - app_start_time)
    return {
        "status": "ok",
        "uptime_seconds": uptime,
        "last_successful_fetch": last_successful_fetch
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
