# Testing Guide
## How to Use the Test Suite

**Last Updated:** 2025-10-23
**Test Suite Version:** 1.0

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Running Tests](#running-tests)
4. [Understanding Test Output](#understanding-test-output)
5. [Coverage Reports](#coverage-reports)
6. [Writing New Tests](#writing-new-tests)
7. [Debugging Failed Tests](#debugging-failed-tests)
8. [Best Practices](#best-practices)
9. [Common Issues](#common-issues)
10. [FAQ](#faq)

---

## Quick Start

**Run all tests:**
```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=app --cov-report=html
```

**View coverage report:**
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## Installation

### Prerequisites
- Python 3.9 or 3.10
- pip package manager
- Virtual environment (recommended)

### Install Dependencies

```bash
# Install all dependencies (production + testing)
pip install -r requirements.txt

# Or install only testing dependencies
pip install pytest pytest-cov pytest-flask pytest-mock responses
```

### Verify Installation

```bash
# Check pytest is installed
pytest --version

# Should output something like:
# pytest 8.4.0
```

---

## Running Tests

### Run All Tests

```bash
# Run all tests with default settings
pytest

# Verbose output (shows each test)
pytest -v

# Very verbose (shows detailed info)
pytest -vv
```

### Run Specific Test Categories

```bash
# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run specific test file
pytest tests/unit/test_weather.py

# Run specific test function
pytest tests/unit/test_weather.py::test_get_weather_success
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run all except slow tests
pytest -m "not slow"
```

### Run Tests in Parallel (Optional)

```bash
# Install pytest-xdist first
pip install pytest-xdist

# Run tests in parallel (4 workers)
pytest -n 4
```

---

## Understanding Test Output

### Successful Test Run

```
============================= test session starts ==============================
platform darwin -- Python 3.9.20, pytest-8.4.0, pluggy-1.6.0
rootdir: /Users/ash/Desktop/SWE40006_GroupProject_SourceCode
configfile: pytest.ini
collected 23 items

tests/integration/test_health.py ..                                      [  8%]
tests/unit/test_forecast.py .............                                [ 65%]
tests/unit/test_weather.py ........                                      [100%]

============================== 23 passed in 1.23s ===============================
```

**Key Information:**
- `.` = Test passed
- `F` = Test failed
- `E` = Test error
- `s` = Test skipped
- `23 passed` = Total passing tests
- `1.23s` = Execution time

### Failed Test Output

```
FAILED tests/unit/test_weather.py::test_get_weather_success - AssertionError

=================================== FAILURES ===================================
_____________________ test_get_weather_success _____________________

    def test_get_weather_success(client):
        result = get_weather("Melbourne")
>       assert result is not None
E       AssertionError: assert None is not None

tests/unit/test_weather.py:25: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_weather.py::test_get_weather_success
========================= 1 failed, 22 passed in 1.15s =========================
```

**How to Read Failure:**
1. **Test Name:** `test_get_weather_success`
2. **File Location:** `tests/unit/test_weather.py:25`
3. **Assertion:** `assert None is not None`
4. **Type:** `AssertionError`

---

## Coverage Reports

### Generate Coverage Report

```bash
# Terminal report only
pytest --cov=app

# Terminal + HTML report
pytest --cov=app --cov-report=html

# Terminal + XML report (for CI/CD)
pytest --cov=app --cov-report=xml

# All report types
pytest --cov=app --cov-report=html --cov-report=xml --cov-report=term
```

### Terminal Coverage Report

```
Name     Stmts   Miss  Cover   Missing
--------------------------------------
app.py      74     13    82%   83-95, 107
--------------------------------------
TOTAL       74     13    82%
```

**Column Meanings:**
- **Stmts:** Total statements in file
- **Miss:** Statements not executed during tests
- **Cover:** Coverage percentage
- **Missing:** Line numbers not covered

### HTML Coverage Report

```bash
# Generate HTML report
pytest --cov=app --cov-report=html

# Open in browser
open htmlcov/index.html
```

**HTML Report Features:**
- Visual coverage highlighting
- Red = Not covered
- Green = Covered
- Click on files to see line-by-line coverage
- Filter by coverage percentage

### Coverage Threshold

Tests fail if coverage < 75%:

```
ERROR: Coverage failure: total of 72 is less than fail-under=75
FAIL Required test coverage of 75% not reached. Total coverage: 72.34%
```

**To change threshold:** Edit `pytest.ini`:
```ini
[pytest]
addopts = --cov-fail-under=75  # Change to desired percentage
```

---

## Writing New Tests

### Test File Structure

```python
"""
Brief description of what this test file tests.

Additional details if needed.
"""

import pytest
# Import what you're testing
from app import function_to_test


@pytest.mark.unit  # or @pytest.mark.integration
def test_descriptive_name():
    """Test description explaining what is being tested."""
    # Arrange - Set up test data
    input_data = "test"

    # Act - Call the function
    result = function_to_test(input_data)

    # Assert - Verify results
    assert result == expected_value
```

### Using Fixtures

Fixtures are defined in `tests/conftest.py` and available to all tests:

```python
def test_health_endpoint(client):
    """The 'client' fixture is automatically provided."""
    response = client.get('/health')
    assert response.status_code == 200
```

**Available Fixtures:**
- `app` - Flask application instance
- `client` - HTTP test client
- `runner` - CLI test runner
- `mock_weather_success` - Mock weather API response
- `mock_forecast_success` - Mock forecast API response
- `mock_weather_api_error` - Mock error response

### Mocking HTTP Requests

```python
import responses

@responses.activate
def test_api_call():
    # Setup mock response
    responses.add(
        responses.GET,
        'https://api.example.com/data',
        json={'key': 'value'},
        status=200
    )

    # Call your function that makes HTTP request
    result = your_function()

    # Verify result
    assert result is not None
```

### Test Naming Conventions

**Good test names:**
```python
def test_get_weather_success()
def test_get_weather_invalid_city()
def test_health_endpoint_returns_correct_status()
def test_forecast_aggregates_temperatures_correctly()
```

**Bad test names:**
```python
def test1()  # Not descriptive
def test_function()  # Too vague
def test_everything()  # Too broad
```

---

## Debugging Failed Tests

### 1. Run Single Test

```bash
# Run just the failing test
pytest tests/unit/test_weather.py::test_get_weather_success -v
```

### 2. Print Debug Information

```python
def test_something():
    result = function_call()
    print(f"Result: {result}")  # Will show in output
    assert result == expected
```

Run with `-s` to see print statements:
```bash
pytest tests/unit/test_weather.py::test_something -s
```

### 3. Use Debugger

```python
def test_something():
    result = function_call()
    import pdb; pdb.set_trace()  # Debugger breakpoint
    assert result == expected
```

Or use pytest's builtin debugger:
```bash
pytest --pdb  # Drop into debugger on failure
```

### 4. Increase Verbosity

```bash
# Show more details
pytest -vv

# Show full diff for assertions
pytest -vv --tb=long
```

### 5. Check Fixture Values

```python
def test_with_fixture(mock_weather_success):
    print(f"Fixture value: {mock_weather_success}")
    # Continue test...
```

---

## Best Practices

### 1. Test Naming
✅ **DO:**
- Use descriptive, action-oriented names
- Include what is being tested
- Include expected behavior
- Use `test_` prefix

❌ **DON'T:**
- Use generic names like `test1`, `test2`
- Use abbreviations
- Make names too long (> 50 chars)

### 2. Test Structure
✅ **DO:**
- Follow AAA pattern (Arrange, Act, Assert)
- Test one thing per test
- Keep tests independent
- Use fixtures for setup

❌ **DON'T:**
- Test multiple things in one test
- Create interdependent tests
- Repeat setup code across tests
- Use global variables

### 3. Assertions
✅ **DO:**
- Use specific assertions
- Include assertion messages when helpful
- Test expected behavior, not implementation

❌ **DON'T:**
- Use generic `assert True`
- Over-assert (too many assertions)
- Assert on irrelevant details

### 4. Mocking
✅ **DO:**
- Mock external dependencies (APIs, databases)
- Use `responses` for HTTP mocking
- Verify mock was called if important

❌ **DON'T:**
- Mock what you're testing
- Over-mock (makes tests fragile)
- Forget to reset mocks between tests

### 5. Coverage
✅ **DO:**
- Aim for 75%+ coverage
- Focus on critical business logic
- Test edge cases and errors
- Review coverage reports regularly

❌ **DON'T:**
- Chase 100% coverage blindly
- Test trivial code (getters/setters)
- Sacrifice test quality for coverage numbers

---

## Common Issues

### Issue 1: Import Errors

**Problem:**
```
ImportError: cannot import name 'app' from 'app'
```

**Solution:**
```bash
# Ensure you're in project root
cd /path/to/project

# Check Python path
export PYTHONPATH=.

# Or run with Python module syntax
python -m pytest
```

### Issue 2: Coverage Not Working

**Problem:**
```
Coverage warning: Module app was previously imported
```

**Solution:**
```bash
# Use Python module syntax
python -m pytest --cov=app

# Or clear cache
rm -rf .pytest_cache
rm -rf __pycache__
rm -rf tests/__pycache__
```

### Issue 3: Tests Pass Locally But Fail in CI

**Possible Causes:**
1. Environment variables missing
2. Different Python version
3. Timing issues (use fixtures, not sleeps)
4. File paths (use absolute paths)

**Solution:**
```bash
# Test with same Python version as CI
python3.10 -m pytest

# Check environment variables
env | grep -i test
```

### Issue 4: Slow Tests

**Solutions:**
```bash
# Run tests in parallel
pip install pytest-xdist
pytest -n auto

# Profile slow tests
pytest --durations=10

# Skip slow tests
pytest -m "not slow"
```

### Issue 5: Fixtures Not Working

**Problem:**
```
fixture 'client' not found
```

**Solution:**
1. Ensure `conftest.py` exists in `tests/` directory
2. Check fixture name matches exactly
3. Verify `conftest.py` has no syntax errors
4. Clear pytest cache: `rm -rf .pytest_cache`

---

## FAQ

### Q: How often should I run tests?

**A:**
- Before committing code
- Before creating a pull request
- After pulling updates from main
- Continuously during development (use `pytest-watch`)

### Q: What's the difference between unit and integration tests?

**A:**
- **Unit Tests:** Test individual functions in isolation, fast (< 1s)
- **Integration Tests:** Test how components work together, slower (may take several seconds)

### Q: Should I test private functions?

**A:** No, test public interfaces. Private functions are tested indirectly through public functions.

### Q: How do I test async functions?

**A:** Use `pytest-asyncio`:
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### Q: Can I run tests without pytest?

**A:** Yes, but not recommended:
```python
if __name__ == "__main__":
    test_get_weather_success()
```

### Q: How do I skip a test?

**A:**
```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_new_feature():
    pass
```

### Q: How do I mark a test as expected to fail?

**A:**
```python
@pytest.mark.xfail(reason="Known bug #123")
def test_buggy_feature():
    assert buggy_function() == expected
```

### Q: How do I test for exceptions?

**A:**
```python
def test_raises_error():
    with pytest.raises(ValueError) as exc_info:
        function_that_raises()

    assert "error message" in str(exc_info.value)
```

### Q: How do I parametrize tests?

**A:**
```python
@pytest.mark.parametrize("city,expected_temp", [
    ("London", 15.0),
    ("Tokyo", 20.0),
    ("Sydney", 25.0),
])
def test_weather_for_cities(city, expected_temp):
    result = get_weather(city)
    assert result["temp"] == expected_temp
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
- name: Run Tests
  run: |
    pytest --cov=app --cov-report=xml --cov-report=term

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

### Pre-commit Hook Example

```bash
# .git/hooks/pre-commit
#!/bin/sh
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

---

## Additional Resources

### Documentation
- **pytest docs:** https://docs.pytest.org/
- **pytest-cov docs:** https://pytest-cov.readthedocs.io/
- **responses docs:** https://github.com/getsentry/responses

### Test Suite Files
- `TESTING_PLAN.md` - Comprehensive testing strategy
- `TESTING_IMPLEMENTATION.md` - Implementation summary
- `pytest.ini` - Configuration file
- `tests/conftest.py` - Shared fixtures

### Commands Reference

```bash
# Basic
pytest                          # Run all tests
pytest -v                       # Verbose
pytest -vv                      # Very verbose

# Specific tests
pytest tests/unit/              # Unit tests only
pytest tests/integration/       # Integration tests only
pytest -m unit                  # Tests marked as unit
pytest -k "weather"             # Tests matching "weather"

# Coverage
pytest --cov=app                # With coverage
pytest --cov-report=html        # HTML report
pytest --cov-report=term-missing # Show missing lines

# Output control
pytest -s                       # Show print statements
pytest -q                       # Quiet mode
pytest --tb=short               # Short traceback
pytest --tb=no                  # No traceback

# Debugging
pytest --pdb                    # Drop into debugger on failure
pytest --lf                     # Run last failed tests
pytest --ff                     # Run failures first

# Performance
pytest -n auto                  # Parallel execution
pytest --durations=10           # Show slowest 10 tests
```

---

## Getting Help

### In the Project
1. Read this guide
2. Check `TESTING_PLAN.md` for strategy
3. Check `TESTING_IMPLEMENTATION.md` for details
4. Review existing tests for examples

### External Resources
1. pytest documentation
2. Stack Overflow
3. Python testing forums
4. Team members

---

**Version:** 1.0
**Maintained By:** Testing Team
**Last Review:** 2025-10-23
**Status:** Production Ready ✅
