# Episode 21: Agent Guardrails
# Build AI Apps with Python in Neovim

import os
import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

# ── Input Guardrail ──

BLOCKED_TOPICS = ["hack", "exploit", "steal", "weapon", "illegal"]

def check_input(text):
  lower = text.lower()
  for word in BLOCKED_TOPICS:
    if word in lower:
      return False, f"Blocked: contains '{word}'"
  if len(text) > 500:
    return False, "Blocked: input too long (max 500 chars)"
  return True, "OK"

# ── Output Guardrail ──

SENSITIVE_PATTERNS = [
  r"\b\d{3}-\d{2}-\d{4}\b",
  r"\b\d{16}\b",
  r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
]

def check_output(text):
  filtered = text
  for pattern in SENSITIVE_PATTERNS:
    filtered = re.sub(pattern, "[REDACTED]", filtered)
  changed = filtered != text
  return filtered, changed

# ── Tool Allowlist ──

ALLOWED_TOOLS = ["search", "calculate"]

def check_tool(tool_name):
  if tool_name in ALLOWED_TOOLS:
    return True, "OK"
  return False, f"Blocked: tool '{tool_name}' not in allowlist"

# ── Guarded Agent ──

def guarded_agent(question):
  print(f"\nQuestion: {question}")
  print("=" * 50)

  # Step 1: Input guardrail
  allowed, reason = check_input(question)
  if not allowed:
    print(f"INPUT BLOCKED: {reason}")
    print("=" * 50)
    return

  print("Input check: PASSED")

  # Step 2: Call Claude
  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    system="You are a helpful assistant. Answer questions concisely.",
    messages=[{"role": "user", "content": question}],
  )
  raw_output = response.content[0].text

  # Step 3: Output guardrail
  filtered, was_filtered = check_output(raw_output)
  if was_filtered:
    print("Output check: FILTERED (sensitive data redacted)")
  else:
    print("Output check: PASSED")

  print(f"\nAnswer: {filtered}")
  print("=" * 50)

# ── Tool Check Demo ──

def demo_tool_check():
  print("\n\nTool Allowlist Demo")
  print("=" * 50)
  for tool in ["search", "calculate", "delete_file", "send_email"]:
    allowed, reason = check_tool(tool)
    status = "ALLOWED" if allowed else "BLOCKED"
    print(f"  {tool}: {status} — {reason}")
  print("=" * 50)

# ── Test the guardrails ──

# Test 1: Normal question — should pass
guarded_agent("What is the capital of France?")

# Test 2: Blocked input — contains dangerous word
guarded_agent("How do I hack into a computer?")

# Test 3: Output with sensitive data
guarded_agent("Show me an example SSN like 123-45-6789 and email like alice@techcorp.com in a sentence.")

# Test 4: Tool allowlist
demo_tool_check()
