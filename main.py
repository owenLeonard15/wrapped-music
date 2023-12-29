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


# accepts image file paths and returns json string of json objects
def parse_images(image_paths):

    base64_images = []
    # Getting the base64 string
    for image_path in image_paths:
        base64_image = encode_image("data/spotify/" + image_path)
        base64_images.append(base64_image)

    # create payload including all base64 images
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
and top genre from each of the following spotify wrapped photos? \
Make guesses for incomplete values. Return a list of valid json objects. \
Each json object should contain a key value pair for each of top_artists, top_songs, minutes_listened, top_genre. \
If any values are missing return null for that value. \
If you cannot parse an image for any reason return an empty json object."
            },
            # all base64 images
            *[{
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "low"
            }
            } for base64_image in base64_images]
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

    parse_string = ""
    # process 100 images at a time
    for i in tqdm(range(0, len(image_paths), 100)):
        # get 100 images
        image_paths_100 = image_paths[i:i+100]
        # parse the images
        parse_string = parse_images(image_paths_100)

        with open(f"response_{i}.json", 'w') as f:
            # remove last comma
            parse_string = parse_string[:-1]
            f.write("["+parse_string+"]")