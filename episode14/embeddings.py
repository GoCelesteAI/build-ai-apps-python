# Episode 14: Embeddings
# Build AI Apps with Python in Neovim

import math

# What is an embedding?
# Text -> list of numbers (a vector)
# Similar text -> similar vectors

# Cosine similarity from scratch
def cosine_similarity(a, b):
  dot_product = sum(x * y for x, y in zip(a, b))
  magnitude_a = math.sqrt(sum(x * x for x in a))
  magnitude_b = math.sqrt(sum(x * x for x in b))
  if magnitude_a == 0 or magnitude_b == 0:
    return 0.0
  return dot_product / (magnitude_a * magnitude_b)

# Simple embedding function using sentence-transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
  return model.encode(text).tolist()

# Test with similar and different sentences
sentences = [
  "The cat sat on the mat",
  "A kitten rested on the rug",
  "Python is a programming language",
  "The weather is sunny today",
]

print("=== Generating embeddings ===")
embeddings = [embed(s) for s in sentences]
print(f"Vector size: {len(embeddings[0])} dimensions\n")

print("=== Similarity scores ===")
for i in range(len(sentences)):
  for j in range(i + 1, len(sentences)):
    score = cosine_similarity(embeddings[i], embeddings[j])
    print(f"{score:.3f}  '{sentences[i]}'")
    print(f"        vs '{sentences[j]}'\n")
