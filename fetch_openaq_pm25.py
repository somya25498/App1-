import requests
import pandas as pd

def fetch_pm25(city="Delhi", limit=1000):
    url = "https://api.openaq.org/v2/measurements"
    params = {
        "city": city,
        "parameter": "pm25",
        "limit": limit,
        "sort": "desc",
        "order_by": "datetime"
    }

    r = requests.get(url, params=params)
    data = r.json()["results"]

    rows = []
    for item in data:
        rows.append({
            "datetime": item["date"]["utc"],
            "location": item["location"],
            "value": item["value"],
            "unit": item["unit"]
        })

    df = pd.DataFrame(rows)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime")

    return df

if _name_ == "_main_":
    df = fetch_pm25("Delhi", 1000)
    print(df.head())
    print(df.tail())
    df.to_csv("delhi_pm25.csv", index=False)
    print("\nSaved as delhi_pm25.csv")