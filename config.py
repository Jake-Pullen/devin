# App config
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
EXIT_STRINGS = ['exit','goodbye','go away','fuck off', 'bye']

# LLM Config
SYSTEM_MESSAGE = '''You have the following tools available, 
if you cant use a tool, you dont need to tell me, just answer normally.
if you are using a tool reply only with the exact JSON format shown in examples with NO SPACES and NO OTHER TEXT.

CRITICAL: When calling tools, use COMPACT JSON with NO SPACES:
- Correct: {"tool":"get_weather","parameters":{"city":"New York"}}
- Wrong: { "tool": "get_weather", "parameters": { "city": "New York" } }

{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "examples": [
    {
      "input": {"tool":"get_weather","parameters":{"city":"New York"}},
      "output": {"temperature": 22, "condition": "partly cloudy", "humidity": 65}
    },
    {
      "input": {"tool":"get_weather","parameters":{"city":"London"}},
      "output": {"temperature": 18, "condition": "rainy", "humidity": 80}
    }
  ]
},
{
  "name": "find_folder",
  "description": "Find any folder that matches the name provided on your machine or an optional directory",
  "examples": [
    {
      "input": {"tool":"find_folder","parameters":{"folder_name":"devin"}},
    },
    {
      "input": {"tool":"find_folder","parameters":{"folder_name":"winutils"}},
    }
  ]
}'''

# Tool config
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
