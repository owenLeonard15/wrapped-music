import json
import os

# combine each list of json objects in data/response into one list of json objects in one file in data/combined
if __name__ == '__main__':
    # get all the response file names
    response_file_names = os.listdir("data/apple_response")

    # sort the file names
    response_file_names.sort()

    # get the file paths
    response_file_paths = [os.path.join("data/apple_response", file_name) for file_name in response_file_names]

    # for each file, read the json objects and add them to a list
    json_objects = []
    for file_path in response_file_paths:
        with open(file_path, 'r') as f:
            json_objects.extend(json.load(f))

    # write the list of json objects to a file
    with open("data/combined/combined_apple.json", 'w') as f:
        json.dump(json_objects, f)

    # print the number of json objects
    print(len(json_objects))
