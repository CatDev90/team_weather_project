import requests
import sqlite3
import argparse
from prettytable import PrettyTable


class Weather():


    def fetch_weather_data(self,lat,lon):
        """
        Fetch weather data from the OpenWeatherMap API
        """
        print("Fetching weather data")

        base_url = 'http://api.openweathermap.org/data/2.5/weather?'
        complete_url = f"{base_url}appid={'da2c6e20adb2e4056a5da39327c3f36f'}&lat={lat}&lon={lon}"
        response = requests.get(complete_url)
        
        return response.json()

    
    def parse_api_response(self,data):
        """
        Parse the JSON data returned from the API
        """
        print("Parsing API response")
        weather_data = {
            "city":data["name"],
            "temperature":data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather_conditions": data["weather"][0]["description"]
        }

        return weather_data
    

    def make_a_pretty_table(self,data):
        """
        Create a pretty table to display the weather data
        """
        print("Creating a pretty table")
        table = PrettyTable()
        table.field_names = ["City", "Temperature", "Humidity", "Weather Conditions"]
        table.add_row([data["city"], data["temperature"], data["humidity"], data["weather_conditions"]])
        print(table)


    def get_lat_lon_for_city(self,city):
        """
        Get the latitude and longitude for a given city
        """
        print("Getting latitude and longitude for city")
        base_url = 'http://api.openweathermap.org/geo/1.0/direct?'
        endpoint = f"q={city}&limit=1&appid={'da2c6e20adb2e4056a5da39327c3f36f'}"
        url = f"{base_url}{endpoint}"
        response = requests.get(url)
        data = response.json()
        lat = data[0]["lat"]
        lon = data[0]["lon"]

        print(lat,lon)

        return lat, lon


    def db_operations(self, json_response):
        """
        Perform database operations
        """
        print("Performing database operations")
        # Create a connection to the database
        con = sqlite3.connect('weather.db')
        # Create a cursor object
        curs = con.cursor()

        # Create a table in the database if it does not exist
        curs.execute("""CREATE TABLE IF NOT EXISTS weather(
                        city TEXT,
                        temperature FLOAT,
                        humidity INT,
                        weather_conditions TEXT
        )""")

        # get values from parsed_data for inserting into database
        values = list(json_response.values())

        # Ensure that the data types of the values match the data types defined in your database
        # For example, if 'city' is expected to be a string, 'temperature' a float, 'humidity' an int, and 'weather_conditions' a string:
        values = [str(values[0]), float(values[1]), int(values[2]), str(values[3])]

        # Insert the values into the database
        curs.execute("INSERT INTO weather VALUES (?,?,?,?)", values)

        con.commit()

        # Fetch all the rows from the database
        curs.execute("SELECT ROUND(2) FROM weather")

        # Print the rows
        for row in curs.fetchall():
            print(row)


        # create a dict to store curs.fetchall() data
        data = curs.fetchall()
        print(data)

        con.close()

   


    def hourly_weather_data_fetch(self):
        """
        fetching hourly weather data for input location
        """
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 52.52,
            "longitude": 13.41,
            "past_deays":10,
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m"
        }

        response = requests.get(url, params=params)
        data = response.json()

        table = PrettyTable()
        table.field_names = ["Time", "Wind Speed (10m)", "Temperature (2m)", "Relative Humidity (2m)"]

        for i in range(len(data['hourly']['time'])):
            time = data['hourly']['time'][i]
            wind_speed = data['hourly']['wind_speed_10m'][i]
            temperature = data['hourly']['temperature_2m'][i]
            humidity = data['hourly']['relative_humidity_2m'][i]
            table.add_row([time,wind_speed,temperature,humidity])

        print(table)


    def main(self, **kwargs):
        """
        Main method for the Weather class
        """
        print("Executing Main Function")

        city = kwargs.get('city', 'Belfast')
        lat,lon = self.get_lat_lon_for_city(city)
        weather_data = self.fetch_weather_data(lat, lon)
        parsed_data = self.parse_api_response(weather_data)
        print(parsed_data)
        self.db_operations(parsed_data)
        self.make_a_pretty_table(parsed_data)

        # ---- Calling fuction to output hourly data of of location  ----- #
        self.hourly_weather_data_fetch()




if __name__ == "__main__":
    # Create an instance of the Weather class
    weather = Weather()  
    # Call the main method

    # take argument from client for city
    parser = argparse.ArgumentParser(description='Fetches weather information')
    parser.add_argument("city", help="Enter the city name")
    
    args = parser.parse_args()

    user = weather.main(city=args.city)