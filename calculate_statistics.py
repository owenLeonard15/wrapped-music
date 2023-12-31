import json

if __name__ == '__main__':
    # calculate the top artists, top songs, top genre and average minutes listened from the data in combined.json

    # get the json objects
    json_objects = []
    with open("data/combined/combined.json", 'r') as f:
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

    # get the top songs
    top_songs = {}

    for json_object in json_objects:
        if not json_object:
            continue

        if "top_songs" not in json_object or not json_object["top_songs"]:
            continue

        for song in json_object["top_songs"]:
            if song not in top_songs:
                top_songs[song] = 0
            top_songs[song] += 1
    
    # remove None from the top songs
    if None in top_songs:
        del top_songs[None]
    
    # sort the top songs
    top_songs = dict(sorted(top_songs.items(), key=lambda item: item[1], reverse=True)[:10])
    
    # print the top 10 songs
    print(top_songs)

    
    # get the top genres
    top_genres = {}

    for json_object in json_objects:
        if not json_object:
            continue

        if "top_genre" not in json_object or not json_object["top_genre"]:
            continue

        genre = json_object["top_genre"]
        if genre not in top_genres:
            top_genres[genre] = 0
        top_genres[genre] += 1

    # sort the top genres
    top_genres = dict(sorted(top_genres.items(), key=lambda item: item[1], reverse=True)[:10])

    # print the top genres
    print(top_genres)

    # get the average minutes listened
    minutes_listened = []

    for json_object in json_objects:
        if not json_object:
            continue

        if "minutes_listened" not in json_object or not json_object["minutes_listened"]:
            continue

        # convert the minutes listened to an int
        # remove , from the value if it is a string
        cur_minutes_listened = json_object["minutes_listened"]
        if isinstance(cur_minutes_listened, str):
            cur_minutes_listened = cur_minutes_listened.replace(",", "")
            cur_minutes_listened = int(cur_minutes_listened)
        minutes_listened.append(cur_minutes_listened)



    # calculate the average minutes listened
    average_minutes_listened = sum(minutes_listened) / len(minutes_listened)

    # print the average minutes listened
    print(average_minutes_listened)
    