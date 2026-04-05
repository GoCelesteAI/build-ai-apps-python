# Episode 20: Multi-Agent Systems
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

# Specialized agent: Researcher
def researcher(topic):
  print(f"\n  [Researcher] Researching: {topic}")
  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    system="You are a research specialist. Given a topic, provide 3 key facts. Be concise — one sentence per fact. Number them 1, 2, 3.",
    messages=[{"role": "user", "content": f"Research this topic: {topic}"}],
  )
  result = response.content[0].text
  print(f"  [Researcher] Done.")
  return result

# Specialized agent: Writer
def writer(facts):
  print(f"\n  [Writer] Writing summary from research...")
  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    system="You are a writing specialist. Given research facts, write a clear 2-3 sentence summary for a general audience. No bullet points — flowing prose only.",
    messages=[{"role": "user", "content": f"Write a summary from these facts:\n{facts}"}],
  )
  result = response.content[0].text
  print(f"  [Writer] Done.")
  return result

# Specialized agent: Reviewer
def reviewer(summary):
  print(f"\n  [Reviewer] Reviewing summary...")
  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    system="You are an editorial reviewer. Given a summary, rate it Good or Needs Improvement. If good, say why in one sentence. If it needs work, suggest one specific fix.",
    messages=[{"role": "user", "content": f"Review this summary:\n{summary}"}],
  )
  result = response.content[0].text
  print(f"  [Reviewer] Done.")
  return result

# Supervisor: orchestrates the team
def supervisor(task):
  print(f"\nSupervisor received task: {task}")
  print("=" * 50)

  # Step 1: Delegate to researcher
  print("\nStep 1: Delegating to Researcher...")
  facts = researcher(task)
  print(f"\n  Research results:\n  {facts}")

  # Step 2: Delegate to writer
  print("\nStep 2: Delegating to Writer...")
  summary = writer(facts)
  print(f"\n  Summary:\n  {summary}")

  # Step 3: Delegate to reviewer
  print("\nStep 3: Delegating to Reviewer...")
  review = reviewer(summary)
  print(f"\n  Review:\n  {review}")

  # Final output
  print("\n" + "=" * 50)
  print("FINAL REPORT")
  print("=" * 50)
  print(f"\nTopic: {task}")
  print(f"\nResearch:\n{facts}")
  print(f"\nSummary:\n{summary}")
  print(f"\nReview:\n{review}")
  print("=" * 50)

# Run the multi-agent system
supervisor("The history of the Python programming language")
