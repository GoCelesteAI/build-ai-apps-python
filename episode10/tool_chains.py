# Episode 10: Multi-Step Tool Chains
# Build AI Apps with Python in Neovim

import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

WORK_DIR = "./workspace"
os.makedirs(WORK_DIR, exist_ok=True)

# Tool functions (from Episode 9)
def read_file(path):
  full_path = os.path.join(WORK_DIR, path)
  if not os.path.exists(full_path):
    return {"error": f"File not found: {path}"}
  with open(full_path, "r") as f:
    return {"path": path, "content": f.read()}

def write_file(path, content):
  full_path = os.path.join(WORK_DIR, path)
  with open(full_path, "w") as f:
    f.write(content)
  return {"path": path, "status": "written", "size": len(content)}

def list_directory(path="."):
  full_path = os.path.join(WORK_DIR, path)
  if not os.path.exists(full_path):
    return {"error": f"Directory not found: {path}"}
  items = os.listdir(full_path)
  return {"path": path, "items": items, "count": len(items)}

tool_dispatch = {
  "read_file": read_file,
  "write_file": write_file,
  "list_directory": list_directory,
}

tools = [
  {
    "name": "read_file",
    "description": "Read the contents of a file in the workspace.",
    "input_schema": {
      "type": "object",
      "properties": {
        "path": {"type": "string", "description": "File path"},
      },
      "required": ["path"],
    },
  },
  {
    "name": "write_file",
    "description": "Write content to a file. Creates or overwrites.",
    "input_schema": {
      "type": "object",
      "properties": {
        "path": {"type": "string", "description": "File path"},
        "content": {"type": "string", "description": "Content to write"},
      },
      "required": ["path", "content"],
    },
  },
  {
    "name": "list_directory",
    "description": "List files and folders in the workspace.",
    "input_schema": {
      "type": "object",
      "properties": {
        "path": {"type": "string", "description": "Directory path"},
      },
      "required": ["path"],
    },
  },
]

# The agentic loop — Claude calls tools until done
def agent(task):
  print(f"Task: {task}")
  print("-" * 50)

  messages = [{"role": "user", "content": task}]
  step = 1

  while True:
    response = client.messages.create(
      model="claude-sonnet-4-20250514",
      max_tokens=512,
      tools=tools,
      system="You are a helpful file assistant. Respond in plain text. No markdown.",
      messages=messages,
    )

    if response.stop_reason == "tool_use":
      tool_block = next(b for b in response.content if b.type == "tool_use")
      fn = tool_dispatch[tool_block.name]
      result = fn(**tool_block.input)
      print(f"  Step {step}: {tool_block.name}({tool_block.input})")
      print(f"  Result: {result}")

      messages.append({"role": "assistant", "content": response.content})
      messages.append({
        "role": "user",
        "content": [{"type": "tool_result", "tool_use_id": tool_block.id, "content": json.dumps(result)}],
      })
      step += 1

    else:
      print(f"\n  Final answer: {response.content[0].text}")
      print()
      break

agent("Create a file called notes.txt with three Python tips, then read it back to verify.")
agent("List all files in the workspace, read each one, and write a summary.txt with their contents.")
