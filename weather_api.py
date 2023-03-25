import requests

api_key = "e7704bc895b4a8d2dfd4a29d404285b6"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    resp = requests.get(url)
    data = resp.json()
    print(data)
    precipitation = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    wind_speed = data["wind"]["speed"]
    print(precipitation, wind_speed, temperature)
    return precipitation, wind_speed, temperature
get_weather("Suma")