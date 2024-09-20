# Weather Web App

This Flask application is a weather web app that displays the current temperature, weather forecast, date, moon phase, and helpful tips. It leverages asynchronous functions, connects to an SQLite database, and utilizes third-party libraries for fetching weather data.

## Features

- Current temperature and weather forecast
- Display of the current date and moon phase
- Relevant weather tips

## Instructions

### Installation of Dependencies

Install the necessary dependencies using the following command:

```bash
pip install Flask pytz ephem python_weather
```

Ensure SQLite3 is installed or install it as needed.

### Running the Flask Server

1. Save the provided code in a file named `app.py`.
2. Open a terminal or command prompt.
3. Navigate to the directory containing `app.py`.
4. Run the Flask app:

```bash
flask run
```

5. Open a web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the web app.

> **Note**: Additional steps may be required to set up a virtual environment and handle the database (`database.db`). Ensure the necessary database schema and data are in place.
