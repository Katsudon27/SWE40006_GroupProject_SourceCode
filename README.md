# SWE40006_GroupProject_SourceCode
Weather Dashboard - Flask Application with Comprehensive Testing

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

## Testing Documentation

- **[TESTING_PLAN.md](TESTING_PLAN.md)** - Comprehensive testing strategy
- **[TESTING_IMPLEMENTATION.md](TESTING_IMPLEMENTATION.md)** - What we built
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - How to use the test suite

