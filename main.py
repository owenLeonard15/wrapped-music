from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What are the top 5 artists, top 5 songs, minutes listened, and top genre from this spotify wrapped photo? please return in json format in the order listed above. If any values are missing return null for that value."},
        {
          "type": "image_url",
          "image_url": {
            "url": "",
            "detail": "low"
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])