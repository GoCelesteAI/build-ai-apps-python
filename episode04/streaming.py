# Episode 4: Streaming Responses
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

history = []

print("Streaming Chatbot! Type quit to exit.\n")

while True:
  user_input = input("You: ")
  if user_input.lower() == "quit":
    break

  history.append({"role": "user", "content": user_input})

  print("Claude: ", end="", flush=True)

  with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    system="You are a helpful assistant. Keep responses brief and clear.",
    messages=history,
  ) as stream:
    full_response = ""
    for text in stream.text_stream:
      print(text, end="", flush=True)
      full_response += text

  print("\n")

  history.append({"role": "assistant", "content": full_response})

print("Goodbye!")
