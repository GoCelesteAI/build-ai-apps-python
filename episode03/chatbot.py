# Episode 3: Multi-Turn Conversations
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

history = []

print("Chatbot ready! Type quit to exit.\n")

while True:
  user_input = input("You: ")
  if user_input.lower() == "quit":
    break

  history.append({"role": "user", "content": user_input})

  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=150,
    system="You are a helpful assistant. Keep responses brief and clear.",
    messages=history,
  )

  assistant_message = response.content[0].text
  print(f"\nClaude: {assistant_message}\n")

  history.append({"role": "assistant", "content": assistant_message})

print("Goodbye!")
