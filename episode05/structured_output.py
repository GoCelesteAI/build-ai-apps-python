# Episode 5: Structured Output — JSON Mode
# Build AI Apps with Python in Neovim

import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

system_prompt = """You are a product review analyzer.
Respond ONLY with valid JSON in this exact format:
{
  "sentiment": "positive" or "negative" or "neutral",
  "rating": 1-5,
  "key_points": ["point1", "point2", "point3"],
  "summary": "one sentence summary"
}
No other text. Just JSON."""

def analyze_review(review):
  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    temperature=0.0,
    system=system_prompt,
    messages=[
      {"role": "user", "content": review}
    ],
  )
  return json.loads(response.content[0].text)

review1 = "This laptop is amazing! The battery lasts all day, the screen is gorgeous, and it runs everything I throw at it. Best purchase I made this year."

print("=== Review 1 ===")
result = analyze_review(review1)
print(json.dumps(result, indent=2))

review2 = "Terrible experience. The headphones broke after two weeks, the sound quality was mediocre at best, and customer support was unhelpful."

print("\n=== Review 2 ===")
result = analyze_review(review2)
print(json.dumps(result, indent=2))

review3 = "The coffee maker works fine. Nothing special, nothing terrible. It makes coffee. Does the job for the price."

print("\n=== Review 3 ===")
result = analyze_review(review3)
print(json.dumps(result, indent=2))
