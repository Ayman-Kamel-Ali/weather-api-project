from geopy.geocoders import Nominatim
import requests
import csv

locator = Nominatim(user_agent="my_app")
city = "Cairo"

try:
    location = locator.geocode(city)
    if location is None:
        raise ValueError("City not found")

    lat = location.latitude # type: ignore
    long = location.longitude # type: ignore

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": "temperature_2m,relative_humidity_2m",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    time = data["current"]["time"].split("T")[0]
    temp = data["current"]["temperature_2m"]
    humidity = data["current"]["relative_humidity_2m"]

    print(f"{time} | {city} | {temp}°C | {humidity}%")

    with open("data/weather_data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time, city, temp, humidity])

except Exception as e:
    print("error:", e)
