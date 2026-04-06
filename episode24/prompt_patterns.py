# Episode 24: Prompt Engineering Patterns
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

def ask(system, prompt):
  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    system=system,
    messages=[{"role": "user", "content": prompt}],
  )
  return response.content[0].text

# ── Pattern 1: Zero-Shot vs Few-Shot ──

print("=" * 50)
print("PATTERN 1: Zero-Shot vs Few-Shot")
print("=" * 50)

question = "Classify the sentiment: The battery life is amazing but the screen is too dim."

# Zero-shot
print("\nZero-Shot:")
result = ask(
  "Classify the sentiment as positive, negative, or mixed.",
  question,
)
print(f"  {result}")

# Few-shot
print("\nFew-Shot:")
result = ask(
  "Classify the sentiment as positive, negative, or mixed.",
  """Examples:
"Great product, love it!" -> positive
"Terrible quality, broke in a day." -> negative
"Good features but overpriced." -> mixed

Now classify: The battery life is amazing but the screen is too dim.""",
)
print(f"  {result}")

# ── Pattern 2: Chain-of-Thought ──

print("\n" + "=" * 50)
print("PATTERN 2: Chain-of-Thought")
print("=" * 50)

math_problem = "A store has 24 apples. They sell 8 in the morning and receive a shipment of 15. How many do they have?"

# Direct
print("\nDirect:")
result = ask(
  "Answer the question.",
  math_problem,
)
print(f"  {result}")

# Chain-of-thought
print("\nChain-of-Thought:")
result = ask(
  "Think step by step. Show your reasoning before giving the answer.",
  math_problem,
)
print(f"  {result}")

# ── Pattern 3: Role Prompting ──

print("\n" + "=" * 50)
print("PATTERN 3: Role Prompting")
print("=" * 50)

topic = "Explain what an API is."

# Generic
print("\nGeneric:")
result = ask(
  "You are a helpful assistant.",
  topic,
)
print(f"  {result}")

# Role: Teacher
print("\nRole — Teacher for beginners:")
result = ask(
  "You are a patient teacher explaining to a complete beginner. Use simple analogies. No jargon.",
  topic,
)
print(f"  {result}")

# ── Pattern 4: Output Format Control ──

print("\n" + "=" * 50)
print("PATTERN 4: Output Format Control")
print("=" * 50)

request = "List 3 benefits of code reviews."

# Unformatted
print("\nUnformatted:")
result = ask(
  "You are a helpful assistant.",
  request,
)
print(f"  {result}")

# Formatted
print("\nFormatted (numbered, one line each):")
result = ask(
  "You are a helpful assistant. Respond with a numbered list. One sentence per item. No introductions or conclusions.",
  request,
)
print(f"  {result}")
