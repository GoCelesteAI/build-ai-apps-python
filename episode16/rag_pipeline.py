# Episode 16: The RAG Pipeline
# Build AI Apps with Python in Neovim

import os
from dotenv import load_dotenv
from anthropic import Anthropic
import chromadb

load_dotenv()

client = Anthropic()
db = chromadb.Client()

# Create collection and add knowledge base
collection = db.create_collection(name="knowledge")

docs = [
  "Python was created by Guido van Rossum and first released in 1991. It emphasizes code readability with significant whitespace. Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
  "JavaScript was created by Brendan Eich in 1995 for Netscape Navigator. It is the language of the web browser. Modern JavaScript runs on servers via Node.js and powers frameworks like React, Vue, and Angular.",
  "Rust was created by Mozilla and first released in 2015. It focuses on memory safety without garbage collection. Rust is used for systems programming, web assembly, and building fast command-line tools.",
  "Go was created by Google in 2009. It was designed for simplicity, fast compilation, and built-in concurrency. Go is popular for cloud services, microservices, and DevOps tools like Docker and Kubernetes.",
  "TypeScript was created by Microsoft in 2012. It adds static type checking to JavaScript. TypeScript compiles to plain JavaScript and is widely used in large-scale web applications.",
]

collection.add(
  documents=docs,
  ids=[f"doc_{i}" for i in range(len(docs))],
)

print(f"Knowledge base: {len(docs)} documents loaded\n")

# The RAG pipeline
def ask(question):
  print(f"Q: {question}")

  # Step 1: RETRIEVE — find relevant documents
  results = collection.query(
    query_texts=[question],
    n_results=2,
  )
  docs_found = results["documents"][0]
  context = "\n\n".join(docs_found)
  print(f"  Retrieved {len(docs_found)} relevant documents")

  # Step 2: AUGMENT — build prompt with context
  prompt = f"""Use the following context to answer the question.
If the answer is not in the context, say you do not know.

Context:
{context}

Question: {question}"""

  # Step 3: GENERATE — ask Claude with context
  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    system="Answer based only on the provided context. Respond in plain text only. No markdown, no bullet points, no formatting.",
    messages=[{"role": "user", "content": prompt}],
  )

  print(f"  A: {response.content[0].text}\n")

ask("Who created Python and when?")
ask("What is Rust used for?")
ask("Which language was made by Google?")
