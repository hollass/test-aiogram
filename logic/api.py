import requests

class weather():
    def __init__(self, api_key):
        self.url = 'https://api.openweathermap.org/data/2.5/weather?q='
        self.api_key = api_key
    def get(self, city):
        complete_url = f"{city}&lang=ru&units=metric&appid={self.api_key}"

        response = requests.get(self.url+complete_url)
        data = response.json()

        if data['cod'] != '404':
            main = data['main']
            temperature = main['temp']
            humidity = main['humidity']

            return f"Температура в {city}: {temperature}°C\nВлажность: {humidity}%"
        else:
            return "Город не найден"