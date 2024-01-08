import json

if __name__ == '__main__':
    # calculate the top artists, top songs, top genre and average minutes listened from the data in combined.json

    # get the json objects
    json_objects = []
    with open("data/combined/combined_apple.json", 'r') as f:
        json_objects = json.load(f)
    

    # get the top artists
    top_artists = {}
    for json_object in json_objects:
        if not json_object:
            continue

        if "top_artists" not in json_object or not json_object["top_artists"]:
            continue

        
        for artist in json_object["top_artists"]:
            if artist not in top_artists:
                top_artists[artist] = 0
            top_artists[artist] += 1
    
    # remove None from the top artists
    if None in top_artists:
        del top_artists[None]

    # sort the top artists
    top_artists = dict(sorted(top_artists.items(), key=lambda item: item[1], reverse=True)[:10])

    # print the top artists
    print(top_artists)
    