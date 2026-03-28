# Episode 7: Your First Tool — Currency Converter
# Build AI Apps with Python in Neovim

import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

# Mock exchange rates
RATES = {
  "USD": 1.0,
  "SGD": 1.34,
  "EUR": 0.92,
  "GBP": 0.79,
  "JPY": 149.50,
  "MYR": 4.47,
}

def convert_currency(amount, from_currency, to_currency):
  from_rate = RATES.get(from_currency.upper())
  to_rate = RATES.get(to_currency.upper())
  if not from_rate or not to_rate:
    return {"error": f"Unknown currency: {from_currency} or {to_currency}"}
  usd = amount / from_rate
  result = round(usd * to_rate, 2)
  return {"amount": result, "from": from_currency, "to": to_currency}

# Define the tool for Claude
tools = [
  {
    "name": "convert_currency",
    "description": "Convert an amount from one currency to another. Supported: USD, SGD, EUR, GBP, JPY, MYR.",
    "input_schema": {
      "type": "object",
      "properties": {
        "amount": {"type": "number", "description": "The amount to convert"},
        "from_currency": {"type": "string", "description": "Source currency code"},
        "to_currency": {"type": "string", "description": "Target currency code"},
      },
      "required": ["amount", "from_currency", "to_currency"],
    },
  }
]

# Ask Claude a question that needs the tool
message = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=1024,
  tools=tools,
  messages=[
    {"role": "user", "content": "How much is 100 USD in Singapore dollars?"}
  ],
)

print("Claude response:")
print(json.dumps(json.loads(message.model_dump_json()), indent=2))

# Check if Claude wants to use a tool
if message.stop_reason == "tool_use":
  tool_block = next(b for b in message.content if b.type == "tool_use")
  print(f"\nClaude wants to call: {tool_block.name}")
  print(f"With arguments: {json.dumps(tool_block.input, indent=2)}")

  # Execute the tool
  result = convert_currency(**tool_block.input)
  print(f"\nTool result: {result}")

  # Send the result back to Claude
  final = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[
      {"role": "user", "content": "How much is 100 USD in Singapore dollars?"},
      {"role": "assistant", "content": message.content},
      {
        "role": "user",
        "content": [
          {
            "type": "tool_result",
            "tool_use_id": tool_block.id,
            "content": json.dumps(result),
          }
        ],
      },
    ],
  )

  print(f"\nClaude final answer:")
  print(final.content[0].text)
