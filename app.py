from flask import Flask, render_template, request, redirect, url_for
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Replace with your OpenWeather API key
OPENWEATHER_API_KEY = "10f06fb8ffb771edcc0e37142cc5f021"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather = get_weather(city)
            if not weather:
                error = "Could not fetch weather data. Please try again."
        else:
            error = "Please enter a city name."
    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
