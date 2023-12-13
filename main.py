import base64
import requests
import os

# get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "path_to_your_image.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What are the top 5 artists, top 5 songs, minutes listened, \
            and top genre from this spotify wrapped photo? please return in json \
            format in the order listed above. If any values are missing return null for that value."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}",
            "detail": "low"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

# response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# print(response.json())

# print(response.choices[0])