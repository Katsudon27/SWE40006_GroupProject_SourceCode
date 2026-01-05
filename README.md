# Weather Dashboard - Flask Application

Welcome to the **Weather Dashboard**, a Flask-based web application that provides real-time weather data and a 5-day forecast for any city. This project demonstrates the integration of APIs, responsive web design, and comprehensive testing, along with a CI/CD pipeline for streamlined development and deployment.

---

## Table of Contents
- [Weather Dashboard - Flask Application](#weather-dashboard---flask-application)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Quick Start](#quick-start)
    - [Running the App](#running-the-app)
    - [Running Tests](#running-tests)
  - [Testing Summary](#testing-summary)
  - [CI/CD Pipeline](#cicd-pipeline)

---
## Overview

The **Weather Dashboard** allows users to:
- Search for current weather conditions in any city.
- View a 5-day weather forecast with daily high and low temperatures.
- Access a health check endpoint to monitor the app's uptime and API fetch status.

This project was built as part of the SWE40006 Group Project, focusing on creating a robust, user-friendly application with a strong emphasis on testing and automation.

---

## Features

- **Real-Time Weather Data**: Fetches current weather conditions using the OpenWeather API.
- **5-Day Forecast**: Displays a forecast with daily high/low temperatures and weather icons.
- **Error Handling**: Provides user-friendly error messages for invalid city names or API issues.
- **Responsive Design**: Built with Bootstrap for a clean and mobile-friendly interface.
- **Health Check Endpoint**: Monitors app uptime and last successful API fetch.

---

## Quick Start

### Running the App

**Using Docker:**
```bash
docker build -t weather-dashboard .
docker run -e OPENWEATHER_API_KEY="your_actual_key" -p 5000:5000 weather-dashboard
```

**Locally (without Docker):**
```bash
# Create .env file
touch .env
# Copy contents from .env.example and add your API key

# Run the app
python app.py
```

### Running Tests

**Run all tests:**
```bash
pytest
```

**With coverage:**
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View coverage report
```

## Testing Summary

This project includes a comprehensive testing strategy to ensure reliability and maintainability. The testing process is documented in the following files:

- **[TESTING_PLAN.md](TESTING_PLAN.md)** - Outlines the testing strategy, including unit, integration, and end-to-end tests.
- **[TESTING_IMPLEMENTATION.md](TESTING_IMPLEMENTATION.md)** - Details the implemented tests and their coverage.
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Provides instructions for running and interpreting the test suite.

## CI/CD Pipeline

The project uses GitHub Actions for Continuous Integration and Continuous Deployment (CI/CD). The pipeline includes the following steps:

- Code Linting: Ensures code quality using tools like flake8.
- Automated Testing: Runs the test suite with pytest to verify functionality.
- Build and Deployment: Builds the Docker image and deploys it to the target environment.
This pipeline ensures that every code change is tested and deployed seamlessly, reducing the risk of introducing bugs into production.
