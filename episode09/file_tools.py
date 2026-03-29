# Episode 9: File System Tools
# Build AI Apps with Python in Neovim

import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

WORK_DIR = "./workspace"
os.makedirs(WORK_DIR, exist_ok=True)

# Tool 1: Read a file
def read_file(path):
  full_path = os.path.join(WORK_DIR, path)
  if not os.path.exists(full_path):
    return {"error": f"File not found: {path}"}
  with open(full_path, "r") as f:
    return {"path": path, "content": f.read()}

# Tool 2: Write a file
def write_file(path, content):
  full_path = os.path.join(WORK_DIR, path)
  with open(full_path, "w") as f:
    f.write(content)
  return {"path": path, "status": "written", "size": len(content)}

# Tool 3: List directory
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
        "path": {"type": "string", "description": "File path relative to workspace"},
      },
      "required": ["path"],
    },
  },
  {
    "name": "write_file",
    "description": "Write content to a file in the workspace. Creates or overwrites.",
    "input_schema": {
      "type": "object",
      "properties": {
        "path": {"type": "string", "description": "File path relative to workspace"},
        "content": {"type": "string", "description": "Content to write"},
      },
      "required": ["path", "content"],
    },
  },
  {
    "name": "list_directory",
    "description": "List files and folders in the workspace directory.",
    "input_schema": {
      "type": "object",
      "properties": {
        "path": {"type": "string", "description": "Directory path relative to workspace"},
      },
      "required": ["path"],
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
    print(f"  Tool: {tool_block.name}")
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
  else:
    print(f"  A: {message.content[0].text}\n")

ask("Create a file called hello.txt with the text: Hello from Claude!")
ask("What files are in the workspace?")
ask("Read the contents of hello.txt")
