# Episode 2: System Prompts and Parameters
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

question = "What is the best way to learn programming?"

# Pirate persona
print("=== Pirate ===")
response = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=256,
  system="You are a pirate. Speak like a pirate in every response.",
  messages=[
    {"role": "user", "content": question}
  ],
)
print(response.content[0].text)

# Chef persona
print("\n=== Chef ===")
response = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=256,
  system="You are a chef. Relate everything to cooking and food.",
  messages=[
    {"role": "user", "content": question}
  ],
)
print(response.content[0].text)

# Tutor persona
print("\n=== Tutor ===")
response = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=256,
  system="You are a patient tutor. Give clear, step-by-step advice.",
  messages=[
    {"role": "user", "content": question}
  ],
)
print(response.content[0].text)

# Temperature comparison
print("\n=== Temperature 0.0 ===")
response = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=128,
  temperature=0.0,
  messages=[
    {"role": "user", "content": "Name three fruits."}
  ],
)
print(response.content[0].text)

print("\n=== Temperature 1.0 ===")
response = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=128,
  temperature=1.0,
  messages=[
    {"role": "user", "content": "Name three fruits."}
  ],
)
print(response.content[0].text)
