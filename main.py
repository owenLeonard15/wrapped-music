import base64
import requests
import os
from tqdm.auto import tqdm

# get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
# Parse the API response
def parse_response(response):
    res = response.json()["choices"][0]["message"]["content"]
    # remove json from beginning of string
    res = res[5:]
    # remove ''' from beginning and end of string
    res = res[3:-3]
    # remove any newlines from the end of the string
    res = res.rstrip()
    return res


# accepts image file path and returns json string of json object
def parse_image(image_path):

    # Getting the base64 string
    base64_image = encode_image("data/spotify/" + image_path)

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
and top genre from this spotify wrapped photo? \
Make educated guesses for songs or artists that are incomplete. Return in json \
format in the order listed above. If any values are missing return null for that value. \
If you cannot parse the image for any reason return an empty json object."
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

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    # check if response is valid
    if response.status_code != 200:
        raise Exception("Response status code is not 200")
    
    return parse_response(response)


# entry point
if __name__ == "__main__":
    image_paths = os.listdir("data/spotify")

    # parse each image
    complete_json = ""
    # write to file every 100 images
    for i, path in enumerate(tqdm(image_paths)):
        # skip if cannot parse image
        try:
            parse_string = parse_image(path) + ","
            complete_json += parse_string
        except Exception as e:
            print(e)
            print("Error parsing image: " + path)
            continue

        
        if i % 100 == 0:
            with open(f"response_{i}.json", 'w') as f:
                # remove last comma
                complete_json = complete_json[:-1]
                f.write("["+complete_json+"]")
            complete_json = ""


    # remove last comma
    complete_json = complete_json[:-1]

    # write to file any remaining images
    with open('response_final.json', 'w') as f:
        f.write("["+complete_json+"]")