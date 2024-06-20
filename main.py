import requests
import sqlite3
import argparse
from prettytable import PrettyTable

class Weather():
    

    def fetch_weather_data(self,lat,lon):
        '''
        Fetch weather data from the OpenWeatherMap API
        '''
        print('Fetching weather data')

        end_point = 'http://api.openweathermap.org/data/2.5/weather?'
        complete_url = f'{end_point}appid={'da2c6e20adb2e4056a5da39327c3f36f'}&lat={lat}&lon={lon}'
        response = requests.get(complete_url)

        return response.json()
    
    def main(self, **kwargs):
        print('Executing main function')

        city = kwargs.get('city', 'Belfast')
        lat, lon = self.fetch_weather_data(city)


if __name__ == '__main__':
    weather = Weather()

    parser = argparse.ArgumentParser()
    parser.add_argument('city', help='Enter the name of the city you want to search')

    args = parser.parse_args()

    user = weather.main(city=args.city)