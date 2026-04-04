# Episode 15: Vector Store with ChromaDB
# Build AI Apps with Python in Neovim

import chromadb

# Create a ChromaDB client (in-memory)
client = chromadb.Client()

# Create a collection — like a table for vectors
collection = client.create_collection(name="recipes")

# A small recipe knowledge base
recipes = [
  "Chicken Fried Rice: Cook rice and let it cool. Stir-fry diced chicken with garlic and ginger. Add vegetables like peas, carrots, and corn. Push everything to the side, scramble eggs in the center. Mix everything together with soy sauce and sesame oil.",
  "Pasta Carbonara: Boil spaghetti until al dente. Fry pancetta until crispy. Mix egg yolks with grated parmesan cheese. Toss hot pasta with pancetta, then quickly stir in the egg mixture off heat. The residual heat cooks the eggs into a creamy sauce.",
  "Vegetable Stir Fry: Slice bell peppers, broccoli, snap peas, and mushrooms. Heat oil in a wok until smoking. Cook vegetables in batches for 2 minutes each. Combine with garlic sauce made from soy sauce, cornstarch, and chili flakes.",
  "Banana Smoothie: Blend frozen bananas with milk, a spoonful of peanut butter, and honey. Add ice for thickness. Top with granola and sliced almonds. Great for breakfast or post-workout recovery.",
  "Tomato Soup: Roast tomatoes, onion, and garlic at 400F for 30 minutes. Transfer to a pot, add vegetable broth and basil. Blend until smooth. Season with salt, pepper, and a splash of cream.",
  "Grilled Salmon: Season salmon fillets with lemon, dill, salt, and pepper. Grill skin-side down for 4 minutes, flip and cook 3 more minutes. Serve with steamed asparagus and rice.",
]

# Add recipes to the collection
collection.add(
  documents=recipes,
  ids=[f"recipe_{i}" for i in range(len(recipes))],
)

print(f"Added {len(recipes)} recipes to the collection\n")

# Query 1: What can I make with chicken?
print("=== Query 1 ===")
print("Question: What can I make with chicken?\n")
results = collection.query(
  query_texts=["What can I make with chicken?"],
  n_results=2,
)
for i, doc in enumerate(results["documents"][0]):
  dist = results["distances"][0][i]
  print(f"Result {i+1} (distance: {dist:.3f}):")
  print(f"  {doc}\n")

# Query 2: I want something healthy
print("=== Query 2 ===")
print("Question: I want something healthy for breakfast\n")
results = collection.query(
  query_texts=["I want something healthy for breakfast"],
  n_results=2,
)
for i, doc in enumerate(results["documents"][0]):
  dist = results["distances"][0][i]
  print(f"Result {i+1} (distance: {dist:.3f}):")
  print(f"  {doc}\n")

# Query 3: How do I make pasta?
print("=== Query 3 ===")
print("Question: How do I make Italian pasta?\n")
results = collection.query(
  query_texts=["How do I make Italian pasta?"],
  n_results=2,
)
for i, doc in enumerate(results["documents"][0]):
  dist = results["distances"][0][i]
  print(f"Result {i+1} (distance: {dist:.3f}):")
  print(f"  {doc}\n")
