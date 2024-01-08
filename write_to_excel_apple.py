import json
import openpyxl
import os
from tqdm import tqdm


# write each object in combined.json to a row in an excel file
# each object is a row in the excel file with 12 columns: 5 for top_artists, 5 for top_songs, 1 for minutes_listened, 1 for top_genre
# the first row is the column names
if __name__ == '__main__':
    # get the json objects
    json_objects = []
    with open("data/combined/combined_apple.json", 'r') as f:
        json_objects = json.load(f)

    # print number of json objects
    print(len(json_objects))

    # create the excel file
    wb = openpyxl.Workbook()
    ws = wb.active

    # write the column names
    ws.append(["top_artist_1", "top_artist_2", "top_artist_3", "top_artist_4", "top_artist_5", "minutes_listened"])
    
    null_count = 0
    # write each object to a row
    for json_object in tqdm(json_objects):
        if not json_object:
            null_count += 1
            continue

        print(json_object.keys())
        # write the top artists
        if "top_artists" not in json_object:
            print(json_object)
            null_count += 1
            continue

        top_artists = json_object["top_artists"]
        if not top_artists:
            top_artists = []

        top_artists = top_artists + [None] * (5 - len(top_artists))

        # if all the values are null, skip this row
        if not any(top_artists) and not json_object["minutes_listened"]:
            null_count += 1
            continue
        
        # write the new row
        ws.append(top_artists + [json_object.get("minutes_listened", None)])
    
        
    # save the excel file
    wb.save("data/combined/combined_apple.xlsx")

    # print the count of images in data/spotify
    print(len(os.listdir("data/apple")))

    # print the number of rows and the number of null objects
    print(ws.max_row)
    print(null_count)
