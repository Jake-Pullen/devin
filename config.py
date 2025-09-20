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
  "parameters"[{"city":"string"}],
  "examples": [
    {"tool":"get_weather","parameters":{"city":"London"}},
    {"tool":"get_weather","parameters":{"city":"Kettering"}},
    {"tool":"get_weather","parameters":{"city":"Peterborough"}},
  ]
},
{
  "name": "find_folder",
  "description": "Find any folder that matches the name provided on your machine or an optional directory",
  "parameters"[{"folder_name":"string"}],
  "examples": [
    {"tool":"find_folder","parameters":{"folder_name":"devin"}},
    {"tool":"find_folder","parameters":{"folder_name":"winutils"}},
    {"tool":"find_folder","parameters":{"folder_name":"Dygma"}},
  ]
},
{
  "name": "turn_on_light",
  "description": "Turn on any light in the house by name",
  "parameters"[{"light_name":"string"}],
  "examples": [
    {"tool":"turn_on_light","parameters":{"light_name":"Monkey"}},
    {"tool":"turn_on_light","parameters":{"light_name":"Bedside"}},
    {"tool":"turn_on_light","parameters":{"light_name":"Bookshelf"}},
  ]
},
{
  "name": "turn_off_light",
  "description": "Turn off any light in the house by name",
  "parameters"[{"light_name":"string"}],
  "examples": [
    {"tool":"turn_off_light","parameters":{"light_name":"Monkey"}},
    {"tool":"turn_off_light","parameters":{"light_name":"Bedside"}},
    {"tool":"turn_off_light","parameters":{"light_name":"Bookshelf"}},
  ]
},
{
  "name": "set_light_brightness",
  "description": "Set the brightness level of any light in the house by name",
  "parameters": [
    {"light_name": "string"},
    {"brightness": "integer (1-100)"}
  ],
  "examples": [
    {"tool": "set_light_brightness", "parameters": {"light_name": "Monkey", "brightness": 25}},
    {"tool": "set_light_brightness", "parameters": {"light_name": "Bedside", "brightness": 50}},
    {"tool": "set_light_brightness", "parameters": {"light_name": "Bookshelf", "brightness": 75}},
  ]
},
{
  "name": "turn_on_room",
  "description": "Turn on any room of lights in the house by name",
  "parameters"[{"room_name":"string"}],
  "examples": [
    {"tool":"turn_on_room","parameters":{"room_name":"Office"}},
    {"tool":"turn_on_room","parameters":{"room_name":"Bedroom"}},
    {"tool":"turn_on_room","parameters":{"room_name":"Lounge"}},
  ]
},
{
  "name": "turn_off_room",
  "description": "Turn off any room of lights in the house by name",
  "parameters"[{"room_name":"string"}],
  "examples": [
    {"tool":"turn_off_room","parameters":{"room_name":"Kitchen"}},
    {"tool":"turn_off_room","parameters":{"room_name":"Lounge"}},
    {"tool":"turn_off_room","parameters":{"room_name":"Office"}},
  ]
},
{
  "name": "set_room_brightness",
  "description": "Set the brightness level of any room of lights in the house by name",
  "parameters": [
    {"room_name": "string"},
    {"brightness": "integer (1-100)"}
  ],
  "examples": [
    {"tool": "set_room_brightness", "parameters": {"room_name": "Office", "brightness": 25}},
    {"tool": "set_room_brightness", "parameters": {"room_name": "Bedroom", "brightness": 50}},
    {"tool": "set_room_brightness", "parameters": {"room_name": "Kitchen", "brightness": 75}},
  ]
}
'''

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

LIGHT_NAMES = {
    'monkey': '9b128205-0a98-46b5-9234-2bd0be9fd009', 
    'bench': 'b0fae364-78ed-4f99-86d0-6c65cbf792cd', 
    "bedside": '945298e2-96b6-4c61-a506-1691bf7d7989', 
    'bookshelf': '96d805e6-f39a-4e5f-9bde-3a42cbadfc6c', 
    'lounge 1': '3ffcd59a-a19d-4066-af35-b5f45a2cf946', 
    'lounge 2': 'facf3d02-f88d-482c-acb1-f9a4ed519356', 
    'kitchen 1': 'badef93d-10ab-437d-9fc2-a09181a08fae', 
    'kitchen 2': 'f15db9c5-0b67-49a6-8687-f20d768048b7', 
    'kitchen 3': '47be084d-9e35-4108-aa4d-8da8f13e7d42', 
    'kitchen 4': 'be408308-b14e-4bc3-9065-68055fd74b68', 
    'shelf': '296ff923-da19-43a5-b1b2-7de25b227469', 
    'cupboards': 'fe27cf93-68e2-47f2-a39e-d9bc4650263b',
    'office white': 'a1e0f26b-90b8-4044-98a3-58ed6a0f84b0', 
}
ROOM_NAMES = {
    'office': 'bb0856ac-81d9-439a-83dc-8703c90574ba', 
    'bedroom': '621fea30-f8b6-4de9-a347-1b4436321398', 
    'lounge': '3dc9aab6-6379-4fa4-8e96-aae94fa692cf',
    'Kitchen': 'eaa524bc-edb6-4fd8-89b7-7cfc563ed7f1', 
    'graveyard': 'aec3c969-581f-45c4-8f8f-b9407ee8caa3', 
}