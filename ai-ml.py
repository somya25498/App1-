import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="aqi_tracker"
)

# Fetch historical AQI and weather data
query = """
SELECT a.date, a.aqi, a.main_pollutant, w.temperature, w.humidity, w.wind_speed
FROM aqi_data a
JOIN weather_data w ON a.date = w.date AND a.location_id = w.location_id
WHERE a.location_id = 1
ORDER BY a.date ASC
"""

df = pd.read_sql(query, conn)
conn.close()

print(df.head())
# Target is AQI
y = df['aqi']

# Features: main_pollutant (encoded) + temperature + humidity + wind_speed
X = df[['main_pollutant', 'temperature', 'humidity', 'wind_speed']]

# Encode categorical variable (main_pollutant)
X = pd.get_dummies(X, columns=['main_pollutant'])

print(X.head())
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
from sklearn.metrics import mean_absolute_error, r2_score

predictions = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, predictions))
print("R2:", r2_score(y_test, predictions))
import joblib

joblib.dump(model, "aqi_model.pkl")
import joblib
model = joblib.load("aqi_model.pkl")
predicted_aqi = model.predict([input_features])
# Example input features vector
input_features = [temperature, humidity, wind_speed, ...]  # plus pollutant encoding

predicted_aqi = model.predict([input_features])
print("Predicted AQI:", predicted_aqi[0])
