# Episode 19: Agent with Memory
# Build AI Apps with Python in Neovim

import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

MEMORY_FILE = "agent_memory.json"

# Load existing memory from file
def load_memory():
  if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE) as f:
      return json.load(f)
  return {}

# Save memory to file
def save_memory(memory):
  with open(MEMORY_FILE, "w") as f:
    json.dump(memory, f, indent=2)

# Tool: save a research note
def save_note(topic, content):
  memory = load_memory()
  if topic not in memory:
    memory[topic] = []
  memory[topic].append(content)
  save_memory(memory)
  return f"Saved note under '{topic}'"

# Tool: recall notes on a topic
def recall_notes(topic):
  memory = load_memory()
  if topic in memory:
    notes = memory[topic]
    return f"Found {len(notes)} notes: " + " | ".join(notes)
  return f"No notes found for {topic}"

# Tool: look up information
def lookup_info(query):
  data = {
    "python history": "Python was created by Guido van Rossum in 1991. Named after Monty Python.",
    "python typing": "Python added type hints in 3.5 via PEP 484. Optional, not enforced at runtime.",
    "rust memory": "Rust uses ownership and borrowing for memory safety. No garbage collector needed.",
    "rust concurrency": "Rust prevents data races at compile time with the ownership system.",
  }
  for key, val in data.items():
    if key in query.lower():
      return val
  return f"No information found for: {query}"

# Tool definitions for Claude
tools = [
  {
    "name": "save_note",
    "description": "Save a research note for later recall",
    "input_schema": {
      "type": "object",
      "properties": {
        "topic": {
          "type": "string",
          "description": "The topic category",
        },
        "content": {
          "type": "string",
          "description": "The note content to save",
        },
      },
      "required": ["topic", "content"],
    },
  },
  {
    "name": "recall_notes",
    "description": "Recall saved notes on a topic",
    "input_schema": {
      "type": "object",
      "properties": {
        "topic": {
          "type": "string",
          "description": "The topic to search for",
        },
      },
      "required": ["topic"],
    },
  },
  {
    "name": "lookup_info",
    "description": "Look up programming topic information",
    "input_schema": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The search query",
        },
      },
      "required": ["query"],
    },
  },
]

# Tool dispatcher
def run_tool(name, args):
  if name == "save_note":
    return save_note(args["topic"], args["content"])
  elif name == "recall_notes":
    return recall_notes(args["topic"])
  elif name == "lookup_info":
    return lookup_info(args["query"])
  return f"Unknown tool: {name}"

# The agent loop with memory
def agent(question):
  print(f"\nQuestion: {question}")
  print("=" * 50)

  messages = [{"role": "user", "content": question}]
  step = 1

  while True:
    response = client.messages.create(
      model="claude-sonnet-4-20250514",
      max_tokens=500,
      system="You are a research assistant with persistent memory. Use lookup_info to find information. Always save important findings with save_note. Use recall_notes to check what you already know before researching. Be concise.",
      tools=tools,
      messages=messages,
    )

    if response.stop_reason == "end_turn":
      for block in response.content:
        if hasattr(block, "text"):
          print(f"\nFinal Answer: {block.text}")
      break

    for block in response.content:
      if hasattr(block, "text") and block.text:
        print(f"\nStep {step} — Think: {block.text}")
      if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        print(f"Step {step} — Act: {tool_name}({tool_input})")

        result = run_tool(tool_name, tool_input)
        print(f"Step {step} — Observe: {result}")

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

# Clean start — remove old memory
if os.path.exists(MEMORY_FILE):
  os.remove(MEMORY_FILE)

# Session 1: Research Python
agent("Research the history of Python and save your findings.")

# Session 2: Research Rust
agent("Research Rust memory management and save your findings.")

# Session 3: Recall from memory — no new lookup needed
agent("What do you remember about Python from your earlier research?")
