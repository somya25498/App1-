import requests

# Your API URL
url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,precipitation,wind_speed_120m,wind_direction_120m,precipitation_probability&current=rain,relative_humidity_2m"

response = requests.get(url)
data = response.json()

# Check the structure of the JSON
print(data.keys())
# Example: using current weather if available
current_weather = data.get('current_weather', {})

temperature = current_weather.get('temperature', 0)
humidity = current_weather.get('relativehumidity', 0)
wind_speed = current_weather.get('windspeed', 0)
precipitation = current_weather.get('rain', 0)

print(temperature, humidity, wind_speed, precipitation)
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="aqi_tracker"
)

query = "SELECT aqi FROM aqi_data WHERE location_id = 1 ORDER BY date DESC LIMIT 7"
historical_aqi = pd.read_sql(query, conn)['aqi'].values
conn.close()

# Combine with weather features
input_features = list(historical_aqi) + [temperature, humidity, wind_speed, precipitation]
print(input_features)
import joblib

model = joblib.load("aqi_model.pkl")
predicted_aqi = model.predict([input_features])
print("Predicted AQI:", predicted_aqi[0])
import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="aqi_tracker"
)
cursor = conn.cursor()

query = "INSERT INTO aqi_data (location_id, date, aqi, main_pollutant, created_at) VALUES (%s, %s, %s, %s, %s)"
cursor.execute(query, (1, datetime.date.today(), predicted_aqi[0], "PM2.5", datetime.datetime.now()))
conn.commit()
conn.close()


