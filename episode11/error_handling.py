# Episode 11: Tool Error Handling and Validation
# Build AI Apps with Python in Neovim

import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

WORK_DIR = "./workspace"
os.makedirs(WORK_DIR, exist_ok=True)

# Tools with try/except error handling
def read_file(path):
  try:
    full_path = os.path.join(WORK_DIR, path)
    if ".." in path:
      return {"error": "Invalid path: directory traversal not allowed"}
    if not os.path.exists(full_path):
      return {"error": f"File not found: {path}"}
    with open(full_path, "r") as f:
      return {"path": path, "content": f.read()}
  except Exception as e:
    return {"error": f"Read failed: {str(e)}"}

def write_file(path, content):
  try:
    if not path.strip():
      return {"error": "Path cannot be empty"}
    if ".." in path:
      return {"error": "Invalid path: directory traversal not allowed"}
    full_path = os.path.join(WORK_DIR, path)
    with open(full_path, "w") as f:
      f.write(content)
    return {"path": path, "status": "written", "size": len(content)}
  except Exception as e:
    return {"error": f"Write failed: {str(e)}"}

def divide(a, b):
  try:
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
      return {"error": "Both values must be numbers"}
    if b == 0:
      return {"error": "Cannot divide by zero"}
    return {"result": a / b}
  except Exception as e:
    return {"error": f"Division failed: {str(e)}"}

tool_dispatch = {
  "read_file": read_file,
  "write_file": write_file,
  "divide": divide,
}

tools = [
  {
    "name": "read_file",
    "description": "Read a file. Returns error if not found.",
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
    "description": "Write a file. Returns error if path is invalid.",
    "input_schema": {
      "type": "object",
      "properties": {
        "path": {"type": "string", "description": "File path"},
        "content": {"type": "string", "description": "Content"},
      },
      "required": ["path", "content"],
    },
  },
  {
    "name": "divide",
    "description": "Divide two numbers. Returns error for zero or invalid input.",
    "input_schema": {
      "type": "object",
      "properties": {
        "a": {"type": "number", "description": "Numerator"},
        "b": {"type": "number", "description": "Denominator"},
      },
      "required": ["a", "b"],
    },
  },
]

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
      system="You are a helpful assistant. Respond in plain text. No markdown. If a tool returns an error, explain what went wrong and try a different approach.",
      messages=messages,
    )

    if response.stop_reason == "tool_use":
      tool_blocks = [b for b in response.content if b.type == "tool_use"]
      tool_results = []
      for tool_block in tool_blocks:
        fn = tool_dispatch[tool_block.name]
        result = fn(**tool_block.input)
        print(f"  Step {step}: {tool_block.name}({tool_block.input})")
        print(f"  Result: {result}")
        tool_results.append({"type": "tool_result", "tool_use_id": tool_block.id, "content": json.dumps(result)})
        step += 1

      messages.append({"role": "assistant", "content": response.content})
      messages.append({"role": "user", "content": tool_results})
    else:
      print(f"\n  Answer: {response.content[0].text}")
      print()
      break

agent("Read the file secret.txt")
agent("Divide 100 by 0, then try dividing 100 by 4")
agent("Write a greeting to hello.txt, then read it back")
