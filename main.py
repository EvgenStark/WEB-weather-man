import requests
from flask import render_template, request, Flask
from datetime import datetime, timedelta

app = Flask(__name__)

TOKEN = "cd5bff61b698ebc41c853c415e076fff"


def get_weather_7(city, token):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={token}"
        response = requests.get(url)

        city = response.json()['city']['name']
        country = response.json()['city']['country']

        data = response.json()['list']
        forecast = data
        container = list()
        for day in range(7):
            temperature = round(forecast[day]["main"]["temp"] - 273.15, 1)
            pressure = forecast[day]["main"]["pressure"]
            humidity = forecast[day]["main"]["humidity"]
            date = (datetime.now() + timedelta(days=day)).date()
            container.append((city, country, temperature, pressure, humidity, date))
        return container
    except:
        return False


@app.route('/', methods=["POST", "GET"])
@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        search = request.form['search']
        response = get_weather_7(search, TOKEN)
        if response:
            return render_template('weather.html', container=response)
        return render_template('errors.html')
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888)
