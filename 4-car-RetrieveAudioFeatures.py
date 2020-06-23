import pandas as pd
import spotipy
import spotipy.util as util
import pprint

CLIENT_ID = ""
CLIENT_SECRET = ""
USER = ""
AUDIO_FEATURES = ["acousticness", "danceability", "energy", "instrumentalness", "key", "liveness", "loudness",
                  "speechiness", "tempo", "valence"]

col_names = ['id', 'artist', 'title', 'category_id', 'spotify_id', "acousticness", "danceability", "energy",
             "instrumentalness", "key", "liveness", "loudness", "speechiness", "tempo", "valence"]
res_df = pd.DataFrame(columns=col_names)

dat = pd.read_csv('data\\car\\car_songs.csv', delimiter=',')
pp = pprint.PrettyPrinter(depth=6)

# Spotify authentication
token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

other = {"The Thrill is Gone": "4NQfrmGs9iQXVQI9IpRhjM", "I Like - Jost Grubert Radio Mix": "6YyL7wKVozxjgx5E0bX1Bw",
         "Einer von Zweien": "1Wgkake1IWYYR4o58SFWwP", "One World One Flame": "0GHzhRAicXW0ojZl99Kobc",
         "Hoffnung": "4OSMCbOc4dAgnjNcihsLeQ", "Alles kann besser werde": "4nwZ1TyLyV6FLgLByLGS3J",
         "Eingeliebt - ausgeliebt": "58wWIW6xyC7vgNaTe9LhUS", "Mein Stern": "3YhGKzmwSnKLyyhZeHwKPN",
         "I Cant Dance Alone": "1Ra3Hdx3e2gqhTLFbecvYQ", "Feel It": "4ZuzA7bJPki9xqArptIjIe",
         "Narcotic": "3B9eypU2TJd4JM4sWvRntQ", "Brandenburg Concerto 3": "4tXktBBrKGTebkYjvzFA3i", "Komm Zur Ruhr":
             "6lTb1QKhBExob6UX9hDKOU", "Wishing You Well": "6crMwtkIZG9Qaiq2VnKrXB", "Hallelujah":
             "5IaR621NoOM6i5KTcuNRHM", "Empire State Of Mind": "2igwFfvr1OAGX9SKDCPBwO", "Everybody Hurts":
             "6GqEPMwMhIxKEbIr0cXkrz", "Krieger des Lichts": "4ig5yrQLjlT10HzZDPV1cG", "Disco Pogo":
             "4wil8JATEZTC8GmVCpP3oJ", "No Woman No Cry": "3PQLYVskjUeRmRIfECsL0X"}

all_songs = []

for index, row in dat.iterrows():
    res = spotify.search(f'{row["artist"]} {row["title"]}', limit=3)
    print(row['artist'], row['title'])
    if res['tracks']['total'] == 0 and row["title"] in other:
        song_id = other[row["title"]]
    else:
        song_id = res['tracks']['items'][0]['id']
    af_res = spotify.audio_features([song_id])
    for afs in af_res:
        song = {'id': row['id'], 'artist': row["artist"], 'title': row["title"], 'category_id': row["category_id"],
                'spotify_id': song_id, 'acousticness': afs['acousticness'], 'danceability': afs['danceability'],
                'energy': afs['energy'], 'instrumentalness': afs['instrumentalness'], 'key': afs['key'], 'liveness':
                    afs['liveness'], 'loudness': afs['loudness'], 'speechiness': afs['speechiness'],
                'tempo': afs['tempo'],
                'valence': afs['valence']}
        all_songs.append(song)

res_df = pd.DataFrame(all_songs)
res_df.sort_values('id').to_csv('output\\car\\car_audio_features.csv', index=False)


def normalize_data():
    dat = pd.read_csv('output\\car\\car_audio_features.csv', delimiter=',')
    dat['loudness'] = dat['loudness'].apply(lambda x: (x + 40) / 40)
    dat['tempo'] = dat['tempo'].apply(lambda x: x / 220)

    for af in AUDIO_FEATURES:
        dat[af] = dat[af].apply(lambda x: round(x, 4))

    dat.to_csv('output\\car\\car_audio_features.csv', index=False)


normalize_data()
