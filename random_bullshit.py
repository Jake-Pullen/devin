# def ask_name() -> str:
#     """Ask for a name and keep asking until it's not empty."""
#     while True:
#         name = Prompt.ask("[bold cyan]What is your name?[/]")
#         if name.strip():
#             return name.strip()
#         console.print("[red]Name cannot be empty![/]", style="bold")

# def ask_age() -> int:
#     """Ask for age and validate it's a positive integer."""
#     while True:
#         age_str = Prompt.ask("[bold cyan]How old are you?[/]")
#         try:
#             age = int(age_str)
#             if age <= 0:
#                 raise ValueError
#             return age
#         except ValueError:
#             console.print("[red]Please enter a valid positive integer.[/]", style="bold")

pre_prompt = '''{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {"type": "string", "description": "City name"},
      "units": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "Temperature units"}
    },
    "required": ["city"]
  },
  "examples": [
    {
      "input": {"city": "New York", "units": "celsius"},
      "output": {"temperature": 22, "condition": "partly cloudy", "humidity": 65}
    },
    {
      "input": {"city": "London"},
      "output": {"temperature": 18, "condition": "rainy", "humidity": 80}
    }
  ]
}'''

# def get_weather(city, units="celsius"):
#     # Your logic here (API calls, calculations, etc.)
#     return {"temperature": 25, "condition": "sunny"}