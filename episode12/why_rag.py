# Episode 12: Why RAG?
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

# A fictional company handbook (Claude has never seen this)
handbook = """
Acme Corp Employee Handbook - 2026 Edition

Remote Work Policy:
All employees may work remotely up to 3 days per week.
Remote work requires manager approval via the WorkFlex portal.
Fridays are mandatory in-office collaboration days.

Leave Policy:
Annual leave: 18 days per year for all full-time employees.
Sick leave: 14 days per year, no doctor note needed for 1-2 days.
Parental leave: 16 weeks fully paid for all new parents.

Tech Allowance:
Every employee receives $2,500 per year for equipment.
Claims are submitted through the TechGear portal.
Approved items: laptops, monitors, keyboards, ergonomic chairs.
"""

question = "How many days of annual leave do Acme Corp employees get?"

# Without RAG — Claude does not know about Acme Corp
print("=== Without RAG ===")
response = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=200,
  system="Respond in plain text. No markdown. Be honest if you do not know.",
  messages=[
    {"role": "user", "content": question}
  ],
)
print(response.content[0].text)

# With RAG — inject the handbook as context
print("\n=== With RAG ===")
rag_message = f"""Use the following document to answer the question.

Document:
{handbook}

Question: {question}"""

response = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=200,
  system="Respond in plain text. No markdown. Answer based only on the provided document.",
  messages=[
    {"role": "user", "content": rag_message}
  ],
)
print(response.content[0].text)

# Second question
question2 = "What is the tech allowance and how do I claim it?"

print("\n=== Without RAG ===")
response = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=200,
  system="Respond in plain text. No markdown. Be honest if you do not know.",
  messages=[
    {"role": "user", "content": question2}
  ],
)
print(response.content[0].text)

print("\n=== With RAG ===")
rag_message2 = f"""Use the following document to answer the question.

Document:
{handbook}

Question: {question2}"""

response = client.messages.create(
  model="claude-sonnet-4-20250514",
  max_tokens=200,
  system="Respond in plain text. No markdown. Answer based only on the provided document.",
  messages=[
    {"role": "user", "content": rag_message2}
  ],
)
print(response.content[0].text)
