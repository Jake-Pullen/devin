import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry
import json

# WMO Weather interpretation codes mapping
WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear", 
    2: "Partly cloudy", 
    3: "Overcast",
    45: "Fog", 
    48: "Depositing rime fog",
    51: "Light drizzle", 
    53: "Moderate drizzle", 
    55: "Dense drizzle",
    56: "Light freezing drizzle", 
    57: "Dense freezing drizzle",
    61: "Slight rain", 
    63: "Moderate rain", 
    65: "Heavy rain",
    66: "Light freezing rain", 
    67: "Heavy freezing rain",
    71: "Slight snow", 
    73: "Moderate snow", 
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers", 
    81: "Moderate rain showers", 
    82: "Violent rain showers",
    85: "Slight snow showers", 
    86: "Heavy snow showers",
    95: "Thunderstorm", 
    96: "Thunderstorm with slight hail", 
    99: "Thunderstorm with heavy hail"
}

class ToolExecutor:
    def __init__(self):
        self.tools = {
            "get_weather": self.get_weather
        }
    
    def process_llm_response(self, llm_output):           
        
        # Parse the tool call from LLM response
        if llm_output.startswith('{"tool":'):

            llm_output = json.loads(llm_output)
            
            print(llm_output)
            tool_name = llm_output.get("tool",'no tool')
            parameters = llm_output.get("parameters", 'no parameters')
            print(f'parsed tool: {tool_name}, parsed parameters: {parameters}')
            
            # Execute the actual function
            result = self.tools[tool_name](**parameters)
            
            # Return result for LLM to use
            return result
        return llm_output
    
    def get_weather(self, city: str, units: str = "celsius"):
        """Get current weather for a location using Open-Meteo API with openmeteo-requests library."""
        
        print(f'get weather called, city = {city}')
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
            print(f'Geo data for city: {geo_data}')
            
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
            print(f'Weather API response: {response}')

            # Get current weather data
            current = response.Current()
            print(f'Current weather data: {current}')
            
            # Extract values using the library's methods
            temperature = current.Variables(0).Value()  # temperature_2m
            humidity = current.Variables(1).Value()     # relative_humidity_2m
            weather_code = int(current.Variables(2).Value())  # weather_code
            pressure = current.Variables(3).Value()    # surface_pressure
            wind_speed = current.Variables(4).Value()  # wind_speed_10m
            
            condition = WEATHER_CODE_MAP.get(weather_code, "Unknown")
            

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
            print(json_reply)
            return json_reply
            
        except Exception as e:
            raise Exception(f"Weather lookup failed: {str(e)}")