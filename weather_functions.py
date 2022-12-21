import requests
import time
import datetime

def get_weather(city: str, open_weather_token: str) -> str:

    emoji = {
        "Thunderstorm": "Гроза \U000026C8",
        "Drizzle": "Мелкий дождь \U0001F326",
        "Rain": "Дождь \U0001F327",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
        "Smoke": "Дым \U0001F32B",
        "Fog": "Туман \U0001F32B",
        "Tornado": "Ураган \U0001F32A",
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601"
    }

    try:
        rec = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")
        weather_json = rec.json()

        city_name = weather_json["name"]
        temp = weather_json["main"]["temp"]

        if int(weather_json["main"]["feels_like"]) < 0:
            feels_like = f'{weather_json["main"]["feels_like"]}°C \U0001F976'
        elif int(weather_json["main"]["feels_like"]) < 10:
            feels_like = f'{weather_json["main"]["feels_like"]}°C \U0001F616'
        elif int(weather_json["main"]["feels_like"]) < 30:
            feels_like = f'{weather_json["main"]["feels_like"]}°C \U0001F60A'
        else:
            feels_like = f'{weather_json["main"]["feels_like"]}°C \U0001F975'

        weather_description = weather_json["weather"][0]["main"]
        if weather_description in emoji:
            str = emoji[weather_description]
        else:
            str = weather_description

        humidity = weather_json["main"]["humidity"]
        wind = weather_json["wind"]["speed"]
        time_zone = weather_json["timezone"] - 10800
        local_time = datetime.datetime.fromtimestamp(time.time() + time_zone).strftime("%Y-%m-%d %H:%M:%S")
        sunrise = datetime.datetime.fromtimestamp(weather_json["sys"]["sunrise"] + time_zone).strftime("%H:%M:%S")
        sunset = datetime.datetime.fromtimestamp(weather_json["sys"]["sunset"] + time_zone).strftime("%H:%M:%S")

        weather = (
            f'\U0001F3D9 {city_name} \U0001F3D9\nМестное время: {local_time}\nТемпература: {temp}°C {str}\n'
            f'Ощущается как {feels_like}\nВлажность: {humidity}% \U0001F4A6\nВетер: {wind} м/с \U0001F343\n'
            f'Восход: {sunrise} \U0001F305\nЗакат: {sunset} \U0001F307'
        )

    except:
        weather = 'Проверьте название города!'

    return weather

