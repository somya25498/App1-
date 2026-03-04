import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# 1. Load the data you just saved
df = pd.read_csv('colony_prototype.csv')

# 2. Simple Feature Engineering
# We use current pm2_5 and aqi to predict a "target" aqi for the next day
df['target_aqi'] = df['aqi'].shift(-24)  # Shift back 24 hours to create a target
df.dropna(inplace=True)

# 3. Define Features (X) and Target (y)
X = df[['aqi', 'pm2_5']]
y = df['target_aqi']

# 4. Train the Model
# Random Forest is highly accurate for environmental data
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 5. Save the 'Brain'
joblib.dump(model, 'aqi_model.pkl')
print("✅ AI Model trained and saved as 'aqi_model.pkl'")