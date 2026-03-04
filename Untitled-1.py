# -----------------------------
# AQI Predictor using MySQL + Open-Meteo
# -----------------------------

import requests
import pandas as pd
import mysql.connector
import joblib
import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# -----------------------------
# STEP 1: Fetch Historical AQI from MySQL
# -----------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="aqi_tracker"
)

# Fetch last N days AQI
query = "SELECT date, aqi, main_pollutant FROM aqi_data WHERE location_id = 1 ORDER BY date ASC"
df = pd.read_sql(query, conn)
conn.close()

# Check if we have enough data
if len(df) < 7:
    raise Exception("Not enough historical data. Add at least 7 days of AQI to start.")

# -----------------------------
# STEP 2: Prepare Features and Target for ML Model
# -----------------------------

# Target
y = df['aqi']

# Features
X = df[['main_pollutant']]  # categorical, will encode later

# Encode main_pollutant
X = pd.get_dummies(X, columns=['main_pollutant'])

# -----------------------------
# STEP 3: Train ML Model
# -----------------------------

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print("Model MAE:", mean_absolute_error(y_test, preds))
print("Model R2:", r2_score(y_test, preds))

# Save the model
joblib.dump(model, "aqi_model.pkl")
print("Model saved as aqi_model.pkl")

# -----------------------------
# STEP 4: Fetch Real-Time Weather Data from Open-Meteo
# -----------------------------

url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,precipitation,wind_speed_120m,wind_direction_120m,precipitation_probability&current=rain,relative_humidity_2m"

response = requests.get(url)
data = response.json()

# Extract current weather
current_weather = data.get('current_weather', {})
temperature = current_weather.get('temperature', 0)
humidity = current_weather.get('relativehumidity', 0)
wind_speed = current_weather.get('windspeed', 0)
precipitation = current_weather.get('rain', 0)

print("Weather Data:", temperature, humidity, wind_speed, precipitation)

# -----------------------------
# STEP 5: Prepare Input Features for Prediction
# -----------------------------

# Last 7 days AQI as features
historical_aqi = df['aqi'].tail(7).tolist()

# Note: For categorical main_pollutant, just pick last day for simplicity
last_pollutant = df['main_pollutant'].iloc[-1]

# Encode pollutant same as training
pollutant_encoded = pd.get_dummies(pd.Series([last_pollutant]), columns=None)
# Ensure same columns as training
for col in X.columns:
    if col not in pollutant_encoded.columns:
        pollutant_encoded[col] = 0

pollutant_encoded = pollutant_encoded[X.columns]  # align columns

# Combine AQI + pollutant features (ML model expects this)
input_features = pollutant_encoded.values[0].tolist()

# -----------------------------
# STEP 6: Predict AQI
# -----------------------------

model = joblib.load("aqi_model.pkl")
predicted_aqi = model.predict([input_features])
print("Predicted AQI:", predicted_aqi[0])

# -----------------------------
# STEP 7: Store Predicted AQI in MySQL
# -----------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="aqi_tracker"
)
cursor = conn.cursor()

query = "INSERT INTO aqi_data (location_id, date, aqi, main_pollutant, created_at) VALUES (%s, %s, %s, %s, %s)"
cursor.execute(query, (
    1,
    datetime.date.today(),
    predicted_aqi[0],
    last_pollutant,
    datetime.datetime.now()
))
conn.commit()
conn.close()

print("Predicted AQI stored in database!")
