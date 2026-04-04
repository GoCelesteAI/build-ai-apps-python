# Episode 18: The ReAct Agent Pattern
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

# Tools the agent can use
def lookup_weather(city):
  weather_data = {
    "New York": "72F, sunny",
    "London": "58F, cloudy",
    "Tokyo": "80F, humid",
    "Paris": "65F, rainy",
  }
  return weather_data.get(city, f"No data for {city}")

def calculate(expression):
  try:
    return str(eval(expression))
  except Exception as e:
    return f"Error: {e}"

# Tool definitions for Claude
tools = [
  {
    "name": "lookup_weather",
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
  {
    "name": "calculate",
    "description": "Evaluate a math expression",
    "input_schema": {
      "type": "object",
      "properties": {
        "expression": {
          "type": "string",
          "description": "The math expression to evaluate",
        }
      },
      "required": ["expression"],
    },
  },
]

# Execute a tool call
def run_tool(name, args):
  if name == "lookup_weather":
    return lookup_weather(args["city"])
  elif name == "calculate":
    return calculate(args["expression"])
  return f"Unknown tool: {name}"

# The ReAct agent loop
def agent(question):
  print(f"\nQuestion: {question}")
  print("=" * 50)

  messages = [{"role": "user", "content": question}]
  step = 1

  while True:
    # THINK + ACT: Claude reasons and picks a tool
    response = client.messages.create(
      model="claude-sonnet-4-20250514",
      max_tokens=500,
      system="You are a helpful assistant. Think step by step. Use the provided tools to find information. When you have the final answer, respond directly without using any tools.",
      tools=tools,
      messages=messages,
    )

    # Check if agent is done (no tool use = final answer)
    if response.stop_reason == "end_turn":
      for block in response.content:
        if hasattr(block, "text"):
          print(f"\nFinal Answer: {block.text}")
      break

    # Process each content block
    for block in response.content:
      if hasattr(block, "text") and block.text:
        print(f"\nStep {step} — Think: {block.text}")
      if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        print(f"Step {step} — Act: {tool_name}({tool_input})")

        # OBSERVE: Execute the tool and get result
        result = run_tool(tool_name, tool_input)
        print(f"Step {step} — Observe: {result}")

        # Feed result back to Claude
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
          "role": "user",
          "content": [{
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": result,
          }],
        })
        step += 1

  print("=" * 50)

# Test 1: Single tool use
agent("What is the weather in Tokyo?")

# Test 2: Multi-step reasoning
agent("What is the weather in New York and London? Which city is warmer and by how many degrees?")
