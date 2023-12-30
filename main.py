import time
import base64
import requests
import os
from tqdm.auto import tqdm

# current rate limits: https://platform.openai.com/account/limits

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
    
    # remove ''' from beginning and end of string
    # res = res[1:-1]

    # remove any newlines from the end of the string
    res = res.rstrip()
    return res

# Get the number of tokens left from the API response
# available tokens are returned in response header under x-ratelimit-limit-tokens
def tokens_remaining(response):
    return response.headers['x-ratelimit-remaining-tokens']

def time_until_tokens_reset(response):
    return response.headers['x-ratelimit-reset-tokens']

# accepts image file paths and returns json string of json objects
def parse_images(image_paths):

    base64_images = []
    # Getting the base64 string
    for image_path in image_paths:
        # make sure image is one of the supported types: ['png', 'jpeg', 'gif', 'webp']
        # take lowercase of last element in list
        if image_path.split('.')[-1].lower() not in ['png', 'jpeg', 'jpg', 'gif', 'webp']:
            print(f"Image {image_path} is not a supported type. Skipping...")
            continue
        
        # make sure image is not too large (max 20MB)
        if os.path.getsize("data/spotify/" + image_path) > 20000000:
            print(f"Image {image_path} is too large. Skipping...")
            continue

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
            "text": "List the top 5 artists, top 5 songs, minutes listened, \
and top genre from each of the following spotify wrapped photos. \
Complete any incomplete songs or artists with the full title or artist name. \
Return results in a list of valid json objects. \
Each json object should contain a key value pair for each of top_artists, top_songs, minutes_listened, top_genre. \
If any values are missing return null for that value. \
Skip any images that cannot be parsed. \
Do not include any additional text aside from the list of json objects."
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
    "max_tokens": 4096
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # check if response is valid
    if response.status_code != 200:
        print(response.json())
        raise Exception("Response status code is not 200")
    
    
    return (parse_response(response), tokens_remaining(response), time_until_tokens_reset(response))


# entry point
if __name__ == "__main__":
    image_paths = os.listdir("data/spotify")

    parse_string = ""
    # process batch_count images at a time
    batch_count = 10
    for i in tqdm(range(0, len(image_paths), batch_count)):
        # get batch_count images
        batch_image_paths = image_paths[i:i+batch_count]
        # parse the images
        try:
            parsed_string, tokens_left, time_until_reset = parse_images(batch_image_paths)
        except Exception as e:
            print(e)
            print("Skipping batch...")
            # write skipped images to file:
            with open(f"skipped_{i}.txt", 'w') as f:
                f.write("\n".join(batch_image_paths))
            continue

        with open(f"response_{i}.json", 'w') as f:
            f.write("["+parsed_string+"]")

        print(f"Tokens used: {tokens_left}")
        print(f"Time until tokens reset: {time_until_reset}")
        # sleep for time_until_tokens_reset seconds plus 1 second to be safe
        # example time_until_tokens_reset: '25.242s'
        sleep_time = float(time_until_reset[:-1]) + 1
        time.sleep(sleep_time)
        
