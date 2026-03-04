import sys
import joblib
import json

# Load the trained model
model = joblib.load('aqi_model.pkl')

# Get command line arguments with error handling
if len(sys.argv) < 3:
    print(json.dumps({"error": "Missing arguments"}))
    sys.exit(1)

current_aqi = float(sys.argv[1])
current_pm25 = float(sys.argv[2])

# Predict next 7 days
forecast = []
aqi = current_aqi
pm25 = current_pm25

for day in range(7):
    predicted = model.predict([[aqi, pm25]])[0]
    forecast.append(round(predicted, 2))
    aqi = predicted  # Use prediction as next input
    pm25 = pm25 * 0.98  # Slight decay assumption

# Output as JSON
print(json.dumps(forecast))
