import requests
import pandas as pd
import time
from datetime import datetime, timedelta

API_KEY = "89de5e68472f0225ba881d3d01b68e22"

# 7 Selected Colonies for the Prototype
COLONIES = [
    {"name": "Connaught Place", "lat": 28.6315, "lon": 77.2167},
    {"name": "Dwarka", "lat": 28.5921, "lon": 77.0460},
    {"name": "Okhla", "lat": 28.5450, "lon": 77.2732},
    {"name": "Rohini", "lat": 28.7041, "lon": 77.1025},
    {"name": "Hauz Khas", "lat": 28.5494, "lon": 77.2001},
    {"name": "Janakpuri", "lat": 28.6219, "lon": 77.0878},
    {"name": "Anand Vihar", "lat": 28.6469, "lon": 77.3152}
]

def get_prototype_data(days=30):
    all_data = []
    end_time = int(time.time())
    start_time = int((datetime.now() - timedelta(days=days)).timestamp())

    for colony in COLONIES:
        print(f"Collecting data for: {colony['name']}...")
        url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={colony['lat']}&lon={colony['lon']}&start={start_time}&end={end_time}&appid={API_KEY}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'list' in data:
                for e in data['list']:
                    all_data.append({
                        'colony': colony['name'],
                        'aqi': e['main']['aqi'],
                        'pm2_5': e['components']['pm2_5'],
                        'timestamp': e['dt']
                    })
        time.sleep(1) # Slows down slightly to prevent CPU spikes on your laptop

    df = pd.DataFrame(all_data)
    df.to_csv('colony_prototype.csv', index=False)
    print(f"✅ Success! Saved {len(df)} rows to colony_prototype.csv")

get_prototype_data(30)