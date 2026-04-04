# Episode 17: Multi-Document RAG
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic
import chromadb

load_dotenv()

client = Anthropic()
db = chromadb.Client()

# Create collection for multi-document RAG
collection = db.create_collection(name="company_docs")

# Document sources — each has a filename and content chunks
handbook = [
  "All employees get 20 days of paid time off per year. Unused PTO carries over up to 5 days into the next year. PTO requests must be submitted at least 2 weeks in advance.",
  "The engineering team follows a 2-week sprint cycle. Stand-ups are at 9:30 AM daily. Code reviews require at least 2 approvals before merging.",
  "Remote work is available 3 days per week. Employees must be in office on Tuesday and Thursday. Home office equipment stipend is 500 dollars per year.",
]

faq = [
  "Q: How do I reset my password? A: Go to the IT portal at helpdesk.acme.com and click Forgot Password. You will receive a reset link by email within 5 minutes.",
  "Q: How do I request new software? A: Submit a ticket on the IT portal under Software Requests. Include the software name, license type, and business justification. Approvals take 3 to 5 business days.",
  "Q: Who do I contact for building access? A: Email facilities at facilities@acme.com with your employee ID and the floors you need access to. Badge updates take 24 hours.",
]

policy = [
  "Expenses over 100 dollars require manager approval. Expenses over 1000 dollars require VP approval. All receipts must be submitted within 30 days of purchase.",
  "Company laptops must use full-disk encryption. Personal devices cannot access production systems. Security training is mandatory every 6 months.",
  "The company matching for 401k is 4 percent of salary up to 50000 dollars. Matching vests over 3 years. Enrollment opens in January and July.",
]

# Add all documents with source metadata
all_docs = []
all_ids = []
all_metadata = []

for i, text in enumerate(handbook):
  all_docs.append(text)
  all_ids.append(f"handbook_{i}")
  all_metadata.append({"source": "handbook.txt"})

for i, text in enumerate(faq):
  all_docs.append(text)
  all_ids.append(f"faq_{i}")
  all_metadata.append({"source": "faq.txt"})

for i, text in enumerate(policy):
  all_docs.append(text)
  all_ids.append(f"policy_{i}")
  all_metadata.append({"source": "policy.txt"})

collection.add(
  documents=all_docs,
  ids=all_ids,
  metadatas=all_metadata,
)

print(f"Loaded {len(all_docs)} chunks from 3 documents\n")

# Multi-document RAG with source citations
def ask(question, source_filter=None):
  print(f"Q: {question}")

  # Build query with optional source filter
  query_args = {
    "query_texts": [question],
    "n_results": 3,
  }

  if source_filter:
    query_args["where"] = {"source": source_filter}
    print(f"  [Filter: {source_filter}]")

  # Step 1: RETRIEVE with metadata
  results = collection.query(**query_args)
  docs = results["documents"][0]
  sources = [m["source"] for m in results["metadatas"][0]]
  print(f"  Retrieved {len(docs)} chunks from: {', '.join(set(sources))}")

  # Step 2: AUGMENT with source labels
  context_parts = []
  for doc, src in zip(docs, sources):
    context_parts.append(f"[{src}] {doc}")
  context = "\n\n".join(context_parts)

  prompt = f"""Answer the question using ONLY the provided context.
Cite the source file for each fact in your answer.

Context:
{context}

Question: {question}"""

  # Step 3: GENERATE with citations
  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    system="Answer based only on the provided context. Cite sources as (source: filename). Respond in plain text only. No markdown.",
    messages=[{"role": "user", "content": prompt}],
  )

  print(f"  A: {response.content[0].text}\n")

# Test 1: Cross-document question
ask("How many days off do employees get?")

# Test 2: Filtered to a specific document
ask("How do I reset my password?", source_filter="faq.txt")

# Test 3: Cross-document — security and policy
ask("What are the security requirements?")
