# Import necessary dependencies
from flask import Flask, render_template
import datetime
import pytz
import ephem
import sqlite3
import python_weather
import asyncio
import os
import concurrent.futures

""" Backend Functions """

# Asynchronous function to get the current temperature
async def getCurrentTemp():
    try:
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get('Spain')
            return weather.current.temperature
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Asynchronous function to get the current weather forecast
async def getCurrentForecast():
    try:
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get('Spain')
            forecasts_list = list(weather.forecasts)
            return forecasts_list[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Helper function to run an asynchronous function
def run_asyncio_function(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(func())
    loop.close()
    return result

# Function to get the current date
def getCurrentDate():
    current_time = datetime.datetime.now(pytz.timezone('Etc/GMT+1'))
    month = current_time.month
    day = current_time.day
    year = current_time.year

    if day < 10:
        day = '0' + str(day)
    
    if month < 10:
        month = '0' + str(month)

    return f'{day}/{month}/{year}'

# Function to determine the moon phase based on observer's location
def getMoonPhase():
    observer = ephem.Observer()
    observer.lat = '2.7902'
    observer.lon = '41.6760'

    date = getCurrentDate()
    moon = ephem.Moon(date)
    moon_phase = moon.moon_phase

    if moon_phase < 7.4:
        return "New Moon"
    elif moon_phase < 14.8:
        return "First Quarter"
    elif moon_phase < 22.1:
        return "Full Moon"
    elif moon_phase < 29.5:
        return "Last Quarter"
    else:
        return "New Moon"

# Function to establish a connection to the SQLite database
def getDatabaseCon():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get tips for the current date
def getTipsOfDay():
    conn = getDatabaseCon()
    date = getCurrentDate()
    query = 'SELECT tip FROM tips WHERE date = ?'
    tips = conn.execute(query, (str(date),)).fetchall()
    return tips

# Function to get tips based on the current moon phase
def getMoonTips():
    conn = getDatabaseCon()
    moon_phase = getMoonPhase()

    moon_phase = moon_phase.replace(' ', '_')
    moon_phase = moon_phase.lower()

    query = 'SELECT DISTINCT tip FROM tips WHERE moon_phase = ?'
    tips = conn.execute(query, (str(moon_phase),)).fetchall()
    return tips

""" Flask Server """

# Create a Flask application instance
app = Flask(__name__)

# Flask route for the homepage
@app.route('/')
def index():
    date = getCurrentDate()
    moon_phase = getMoonPhase()
    tipsOfDay = getTipsOfDay()
    moon_tips = getMoonTips()

    tipsOfDayCount = len(tipsOfDay)
    moon_tips_count = len(moon_tips)

    # Adjust asyncio event loop policy for Windows
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Use ThreadPoolExecutor to run asynchronous function concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        temp_future = executor.submit(run_asyncio_function, getCurrentTemp)
    
    temp = temp_future.result()

    # Render the HTML template with the retrieved data
    return render_template('index.html', date=date, moon_phase=moon_phase, tipsOfDay=tipsOfDay, tipsOfDayCount=tipsOfDayCount, moon_tips=moon_tips, moon_tips_count=moon_tips_count, temp=temp)

# Flask route for the weather page
@app.route('/weather')
def weather():
    # Adjust asyncio event loop policy for Windows
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Use ThreadPoolExecutor to run asynchronous function concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        forecast_future = executor.submit(run_asyncio_function, getCurrentForecast)
    
    forecast = forecast_future.result()

    # Render the HTML template with the retrieved weather forecast
    return render_template('weather.html', forecast=forecast)
