import requests
from bs4 import BeautifulSoup

import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('weather_app.ui', self)
        self.showWeatherButton.clicked.connect(self.show_weather)

    def show_weather(self):
        city = self.cityInput.text()
        # Здесь вы можете использовать API погоды
        # Например, @openweathermap.org для получения данных погоды

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        responce = requests.get(f"https://www.google.com/search?q=погода+в+{city}", headers=headers)
        print(responce)

        soup = BeautifulSoup(responce.text, "html.parser")

        temperature = soup.select("#wob_tm")[0].getText()
        title = soup.select("#wob_dc")[0].getText()
        humidity = soup.select("#wob_hm")[0].getText()
        time = soup.select("#wob_dts")[0].getText()
        wind = soup.select("#wob_ws")[0].getText()
        #

        self.weatherLabel.setText(f"Погода в городе: {city}")
        self.weatherDetails.setText(f"{title} {time} Температура: {temperature}C, Влажность: {humidity}, Ветер: {wind}, {responce}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
