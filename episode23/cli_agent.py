# Episode 23: Full-Featured CLI Agent
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

# ── Input Guardrail ──

BLOCKED = ["hack", "exploit", "weapon", "illegal"]

def check_input(text):
  for word in BLOCKED:
    if word in text.lower():
      return False, f"contains '{word}'"
  return True, "OK"

# ── Tool Functions ──

def calculate(expression):
  try:
    return str(eval(expression))
  except Exception as e:
    return f"Error: {e}"

def define_word(word):
  definitions = {
    "algorithm": "A step-by-step procedure for solving a problem",
    "api": "Application Programming Interface — a way for programs to communicate",
    "recursion": "A function that calls itself to solve smaller subproblems",
    "latency": "The delay between a request and a response",
  }
  return definitions.get(word.lower(), f"No definition found for '{word}'")

def get_weather(city):
  weather = {
    "new york": "72F, sunny",
    "london": "58F, cloudy",
    "tokyo": "80F, humid",
  }
  return weather.get(city.lower(), f"No data for {city}")

# ── Tool Definitions ──

tools = [
  {
    "name": "calculate",
    "description": "Evaluate a math expression",
    "input_schema": {
      "type": "object",
      "properties": {
        "expression": {
          "type": "string",
          "description": "The math expression",
        }
      },
      "required": ["expression"],
    },
  },
  {
    "name": "define_word",
    "description": "Look up the definition of a word",
    "input_schema": {
      "type": "object",
      "properties": {
        "word": {
          "type": "string",
          "description": "The word to define",
        }
      },
      "required": ["word"],
    },
  },
  {
    "name": "get_weather",
    "description": "Get the current weather for a city",
    "input_schema": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "The city name",
        }
      },
      "required": ["city"],
    },
  },
]

# ── Tool Dispatcher ──

def run_tool(name, args):
  if name == "calculate":
    return calculate(args["expression"])
  elif name == "define_word":
    return define_word(args["word"])
  elif name == "get_weather":
    return get_weather(args["city"])
  return f"Unknown tool: {name}"

# ── CLI Agent ──

def main():
  print("\nAI Assistant — Tools + Guardrails")
  print("Type a question or quit to exit")
  print("=" * 40)

  messages = []

  while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "quit":
      print("Goodbye!")
      break

    # Input guardrail
    allowed, reason = check_input(user_input)
    if not allowed:
      print(f"  [BLOCKED] {reason}")
      continue

    messages.append({"role": "user", "content": user_input})

    # Agent loop — handles tool use
    while True:
      response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system="You are a helpful assistant with tools. Use calculate for math, define_word for definitions, get_weather for weather. Be concise.",
        tools=tools,
        messages=messages,
      )

      if response.stop_reason == "end_turn":
        for block in response.content:
          if hasattr(block, "text"):
            print(f"\nAssistant: {block.text}")
        messages.append({"role": "assistant", "content": response.content})
        break

      for block in response.content:
        if block.type == "tool_use":
          result = run_tool(block.name, block.input)
          print(f"  [Tool: {block.name}] {result}")
          messages.append({"role": "assistant", "content": response.content})
          messages.append({
            "role": "user",
            "content": [{
              "type": "tool_result",
              "tool_use_id": block.id,
              "content": result,
            }],
          })

main()
