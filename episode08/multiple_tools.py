# Episode 8: Multiple Tools
# Build AI Apps with Python in Neovim

import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

# Tool 1: Currency converter (from Episode 7)
RATES = {
  "USD": 1.0, "SGD": 1.34, "EUR": 0.92,
  "GBP": 0.79, "JPY": 149.50, "MYR": 4.47,
}

def convert_currency(amount, from_currency, to_currency):
  from_rate = RATES.get(from_currency.upper())
  to_rate = RATES.get(to_currency.upper())
  if not from_rate or not to_rate:
    return {"error": "Unknown currency"}
  result = round(amount / from_rate * to_rate, 2)
  return {"amount": result, "from": from_currency, "to": to_currency}

# Tool 2: Weather lookup (mock data)
WEATHER = {
  "singapore": {"temp": 31, "condition": "Partly cloudy", "humidity": 78},
  "tokyo": {"temp": 18, "condition": "Clear", "humidity": 45},
  "london": {"temp": 12, "condition": "Rainy", "humidity": 85},
  "new york": {"temp": 22, "condition": "Sunny", "humidity": 55},
}

def get_weather(city):
  data = WEATHER.get(city.lower())
  if not data:
    return {"error": f"No data for {city}"}
  return {"city": city, **data}

# Tool 3: Time zone lookup (mock data)
TIMEZONES = {
  "singapore": "SGT (UTC+8) — 3:00 PM",
  "tokyo": "JST (UTC+9) — 4:00 PM",
  "london": "GMT (UTC+0) — 7:00 AM",
  "new york": "EST (UTC-5) — 2:00 AM",
}

def get_time(city):
  time = TIMEZONES.get(city.lower())
  if not time:
    return {"error": f"No data for {city}"}
  return {"city": city, "time": time}

# Tool dispatch — maps tool names to functions
tool_dispatch = {
  "convert_currency": convert_currency,
  "get_weather": get_weather,
  "get_time": get_time,
}

# Define all three tools
tools = [
  {
    "name": "convert_currency",
    "description": "Convert an amount from one currency to another.",
    "input_schema": {
      "type": "object",
      "properties": {
        "amount": {"type": "number", "description": "Amount to convert"},
        "from_currency": {"type": "string", "description": "Source currency"},
        "to_currency": {"type": "string", "description": "Target currency"},
      },
      "required": ["amount", "from_currency", "to_currency"],
    },
  },
  {
    "name": "get_weather",
    "description": "Get current weather for a city.",
    "input_schema": {
      "type": "object",
      "properties": {
        "city": {"type": "string", "description": "City name"},
      },
      "required": ["city"],
    },
  },
  {
    "name": "get_time",
    "description": "Get current time in a city.",
    "input_schema": {
      "type": "object",
      "properties": {
        "city": {"type": "string", "description": "City name"},
      },
      "required": ["city"],
    },
  },
]

def ask(question):
  print(f"Q: {question}")
  message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    system="Respond in plain text. No markdown formatting.",
    messages=[{"role": "user", "content": question}],
  )

  if message.stop_reason == "tool_use":
    tool_block = next(b for b in message.content if b.type == "tool_use")
    fn = tool_dispatch[tool_block.name]
    result = fn(**tool_block.input)
    print(f"  Tool: {tool_block.name}({tool_block.input})")
    print(f"  Result: {result}")

    final = client.messages.create(
      model="claude-sonnet-4-20250514",
      max_tokens=1024,
      tools=tools,
      system="Respond in plain text. No markdown formatting.",
      messages=[
        {"role": "user", "content": question},
        {"role": "assistant", "content": message.content},
        {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_block.id, "content": json.dumps(result)}]},
      ],
    )
    print(f"  A: {final.content[0].text}\n")

ask("How much is 50 EUR in Japanese yen?")
ask("What is the weather like in Singapore?")
ask("What time is it in Tokyo?")
