# Weather extract and analysis
This project is about extracting weather data from a website and storing it for analysis. The data is extracted from the API api.openweathermap.org then stored in a database. The data is then analyzed to find the average temperature, humidity, and wind speed for a given city. The data is then visualised using a simple table.
This was a team project, made possible by skilled junior developers: 
Dean Jamieson and M.Angela Stefano

## Installation
Activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

## Usage
Run the script
```bash
python3 weather.py "city_name"
```