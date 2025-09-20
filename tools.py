import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry
import json
import config
import logging
import os
import subprocess
import dotenv
import urllib3

dotenv.load_dotenv()

# Suppress SSL warnings (this is fine for local network)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ToolExecutor:
    def __init__(self, logger):
        self.available_tools = {
            "get_weather": self.get_weather,
            "find_folder": self.find_folder,
            "turn_on_light": self.turn_on_light,
            "turn_off_light": self.turn_off_light,
            "set_light_brightness": self.set_light_brightness,
            "turn_on_room": self.turn_on_room,
            "turn_off_room": self.turn_off_room,
            "set_room_brightness": self.set_room_brightness
        }
        self.logger = logger
        self.bridge_ip = '192.168.0.152'
        self.app_key = os.getenv("USERNAME")
        self.base_url = f'https://{self.bridge_ip}/clip/v2/resource'
        self.session = requests.Session()
        self.session.verify = False  # For local network devices


    def process_llm_response(self, llm_output):
        if llm_output.startswith('{"tool":'):
        # Parse the tool call from LLM response
            llm_output = json.loads(llm_output)

            self.logger.info(f"Parsed LLM output: {llm_output}")
            tool_name = llm_output.get("tool",'no tool')
            parameters = llm_output.get("parameters", 'no parameters')
            self.logger.info(f'parsed tool: {tool_name}, parsed parameters: {parameters}')

            # Execute the actual function
            result = self.available_tools[tool_name](**parameters)

            # Return result for LLM to use
            return result
        return llm_output

    def get_weather(self, city: str, units: str = "celsius"):
        """Get current weather for a location using Open-Meteo API with openmeteo-requests library."""

        self.logger.info(f'get weather called, city = {city}')
        if not city:
            raise ValueError("City parameter is required")

        try:
            # Setup the Open-Meteo API client with cache and retry on error
            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = openmeteo_requests.Client(session=retry_session)

            # Step 1: Get coordinates for the city using geocoding API
            geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
            geocoding_params = {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }

            geo_response = requests.get(geocoding_url, params=geocoding_params, timeout=10)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            self.logger.info(f'Geo data for city: {geo_data}')

            if not geo_data.get("results"):
                raise Exception(f"City '{city}' not found")

            location = geo_data["results"][0]
            latitude = location["latitude"]
            longitude = location["longitude"]
            city_name = location["name"]
            country = location.get("country", "Unknown")

            # Step 2: Get weather data using openmeteo-requests
            url = "https://api.open-meteo.com/v1/forecast"

            # Convert temperature units for the API
            temperature_unit = "celsius" if units == "celsius" else "fahrenheit"

            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "weather_code",
                    "surface_pressure",
                    "wind_speed_10m"
                ],
                "temperature_unit": temperature_unit,
                "wind_speed_unit": "kmh"
            }

            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            self.logger.info(f'Weather API response: {response}')

            # Get current weather data
            current = response.Current()
            self.logger.info(f'Current weather data: {current}')

            # Extract values using the library's methods
            temperature = current.Variables(0).Value()  # temperature_2m
            humidity = current.Variables(1).Value()     # relative_humidity_2m
            weather_code = int(current.Variables(2).Value())  # weather_code
            pressure = current.Variables(3).Value()    # surface_pressure
            wind_speed = current.Variables(4).Value()  # wind_speed_10m

            condition = config.WEATHER_CODE_MAP.get(weather_code, "Unknown")


            json_reply = {
                "temperature": temperature,
                "condition": condition,
                "humidity": humidity,
                "pressure": pressure,
                "wind_speed": wind_speed,
                "units": units,
                "city": city_name,
                "country": country,
                "coordinates": {"latitude": latitude, "longitude": longitude}
            }
            self.logger.info(f"Weather data result: {json_reply}")
            return json_reply

        except Exception as e:
            raise Exception(f"Weather lookup failed: {str(e)}")

    def find_folder(self, folder_name: str, search_path: str = "/home/"):
        """Search for folders with a specific name on the PC."""

        self.logger.info(f'find_folder called, folder_name = {folder_name}, search_path = {search_path}')

        if not folder_name:
            raise ValueError("folder_name parameter is required")

        try:
            found_folders = []
            # Use find command to search for directories
            cmd = ['find', search_path, '-type', 'd', '-name', folder_name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            self.logger.info(result)
            if result.stdout:
                found_folders = [path.strip() for path in result.stdout.split('\n') if path.strip()]

            # Limit results to first 50 to avoid overwhelming output
            found_folders = found_folders[:50]

            json_reply = {
                "folder_name": folder_name,
                "search_path": search_path,
                "found_folders": found_folders,
                "count": len(found_folders)
            }

            self.logger.info(f"Folder search result: {json_reply}")
            return json_reply

        except subprocess.TimeoutExpired:
            raise Exception("Folder search timed out after 30 seconds")
        except Exception as e:
            raise Exception(f"Folder search failed: {str(e)}")

    def tell_hue(self, endpoint, payload):
        headers = {"hue-application-key": self.app_key}
        api_path = self.base_url+endpoint
        return self.session.put(api_path, json=payload, headers=headers, timeout=10)

    def control_light(self, light_name, on_state=True, brightness=None):
        """Control a light"""
        endpoint = f'/light/{config.LIGHT_NAMES[light_name.lower()]}'
        data = {"on": {"on": on_state}}
        if brightness is not None:
            data["dimming"] = {
                "brightness": brightness
            }
        return self.tell_hue(endpoint,data)    
        
    def control_room(self, room_name, on_state=True, brightness=None):
        """Control a light"""
        endpoint = f'/grouped_light/{config.ROOM_NAMES[room_name.lower()]}'
        data = {"on": {"on": on_state}}
        if brightness is not None:
            data["dimming"] = {
                "brightness": brightness
            }
        return self.tell_hue(endpoint,data)

    def turn_on_light(self, light_name):
        return self.control_light(light_name)
    
    def turn_off_light(self, light_name):
        return self.control_light(light_name, on_state=False)

    def set_light_brightness(self, light_name, brightness):
        return self.control_light(light_name, on_state=True, brightness=brightness)
 
    def turn_on_room(self, room_name):
        return self.control_room(room_name)
    
    def turn_off_room(self, room_name):
        return self.control_room(room_name, on_state=False)
    
    def set_room_brightness(self, room_name, brightness):
        return self.control_room(room_name, on_state=True, brightness=brightness)