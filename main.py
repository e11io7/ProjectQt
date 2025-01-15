import sys
import requests
import sqlite3
from bs4 import BeautifulSoup
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication


class WeatherAndNews(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('My App.ui', self)
        connection = sqlite3.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        cursor.execute('SELECT query FROM query_history ORDER BY id DESC LIMIT 1')
        last_query = cursor.fetchone()
        if last_query != None:
            self.cityInput.setText(last_query[0])
            self.run()
        connection.close()
        self.button.clicked.connect(self.run)

    def run(self):
        connection = sqlite3.connect('db.sqlite')
        cursor = connection.cursor()
        city = self.cityInput.text()

        cursor.execute("""
                INSERT INTO query_history (query) VALUES (?)
            """, (city,))

        connection.commit()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        weather = requests.get(f"https://www.google.com/search?q=погода+в+{city}", headers=headers)

        soup = BeautifulSoup(weather.text, "html.parser")

        temperature = soup.select("#wob_tm")[0].getText()
        title = soup.select("#wob_dc")[0].getText()
        humidity = soup.select("#wob_hm")[0].getText()
        time = soup.select("#wob_dts")[0].getText()
        wind = soup.select("#wob_ws")[0].getText()

        f = soup.findAll('span', class_='BBwThe')
        for data in f:
            name = data.text
        if city == '':
            self.cityInput.setText(name)

        news = requests.get(
            f"https://www.google.com/search?sca_esv=434236f4e3901b15&q=новости+{name}&tbm=nws&source=lnms&fbs",
            headers=headers)

        soup = BeautifulSoup(news.text, "html.parser")

        allNews = soup.findAll('div', class_='n0jPhd ynAwRc tNxQIb nDgy9d')
        filteredNews = []
        self.textEdit_2.setText('')

        for data in allNews:
            filteredNews.append(data.text)
            filteredNews.append('\n')
        for data in filteredNews:
            self.textEdit_2.append(data)

        self.textEdit_1.setText(f' {name} \n\n {time} \n {temperature} °C \n {title} \n {humidity} \n {wind}')

        connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherAndNews()
    ex.show()
    sys.exit(app.exec())
