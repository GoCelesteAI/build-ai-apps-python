# Episode 22: Evaluating Agents
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

# A simple agent that answers questions
def agent(question):
  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    system="You are a helpful assistant. Answer concisely in one or two sentences.",
    messages=[{"role": "user", "content": question}],
  )
  return response.content[0].text

# Test cases: question + expected keywords in the answer
test_cases = [
  {
    "question": "What is the capital of France?",
    "expected": ["Paris"],
  },
  {
    "question": "What language is Django written in?",
    "expected": ["Python"],
  },
  {
    "question": "Who created Linux?",
    "expected": ["Linus", "Torvalds"],
  },
  {
    "question": "What does HTML stand for?",
    "expected": ["HyperText", "Markup", "Language"],
  },
  {
    "question": "What year was Python first released?",
    "expected": ["1991"],
  },
]

# Evaluate the agent against test cases
def evaluate(agent_fn, cases):
  print("\nAgent Evaluation")
  print("=" * 60)

  passed = 0
  failed = 0

  for i, case in enumerate(cases):
    question = case["question"]
    expected = case["expected"]

    # Run the agent
    answer = agent_fn(question)

    # Check if all expected keywords appear
    found = []
    missing = []
    for keyword in expected:
      if keyword.lower() in answer.lower():
        found.append(keyword)
      else:
        missing.append(keyword)

    status = "PASS" if not missing else "FAIL"
    if status == "PASS":
      passed += 1
    else:
      failed += 1

    print(f"\nTest {i + 1}: {question}")
    print(f"  Answer: {answer[:60]}...")
    print(f"  {status} — found {found}" + (f" missing {missing}" if missing else ""))

  # Summary
  total = passed + failed
  score = (passed / total) * 100 if total > 0 else 0

  print("\n" + "=" * 60)
  print(f"Results: {passed}/{total} passed ({score:.0f}%)")
  if failed == 0:
    print("All tests passed!")
  else:
    print(f"{failed} test(s) failed.")
  print("=" * 60)

# Run the evaluation
evaluate(agent, test_cases)
