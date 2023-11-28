from fastapi import APIRouter
import requests
from fastapi.responses import JSONResponse

router = APIRouter()

def get_air_temperature_data():
    api_url = "https://api.data.gov.sg/v1/environment/air-temperature"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()

            stations = data['metadata']['stations']
            readings = data['items'][0]['readings']

            temperature_data = {}

            for reading in readings:
                station_id = reading['station_id']
                temperature = reading['value']

                station_details = next((station for station in stations if station['id'] == station_id), None)

                if station_details:
                    station_name = station_details['name']
                    temperature_data[station_name] = temperature

            return temperature_data
        else:
            print(f"Error: Unable to fetch data. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

@router.get("/air_weather")
def get_weather_data():
    air_temperature_data = get_air_temperature_data()
    return air_temperature_data