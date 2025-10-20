# SWE40006_GroupProject_SourceCode
Source Code for SWE40006 Group Project

## Testing
- To test the app using Docker, run the following commands in your terminal after cloning the repo:
  - docker build -t weather-dashboard .
  - docker run -e OPENWEATHER_API_KEY="your_actual_key" -p 5000:5000 weather-dashboard

- To test the app locally without docker after cloning the repo:
  - Run "touch .env" in your directory
  - Copy and paste the contents of .env.example
  - Add API key to the .env file
  - Run "python app.py"
