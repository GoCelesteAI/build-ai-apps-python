# Episode 6: Vision — Image Input
# Build AI Apps with Python in Neovim

import os
import base64
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

def describe_image(image_path):
  with open(image_path, "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

  ext = image_path.split(".")[-1].lower()
  media_type = f"image/{ext}"
  if ext == "jpg":
    media_type = "image/jpeg"

  response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {
              "type": "base64",
              "media_type": media_type,
              "data": image_data,
            },
          },
          {
            "type": "text",
            "text": "Describe this image in detail.",
          },
        ],
      }
    ],
  )

  return response.content[0].text

print("=== Image 1: sunset.png ===")
print(describe_image("sunset.png"))

print("\n=== Image 2: city.png ===")
print(describe_image("city.png"))
