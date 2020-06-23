import time
import pandas as pd
pd.set_option('display.max_columns', None)

cols = ['track_id', "acousticness", "danceability", "energy", "instrumentalness",
        "key", "liveness", "loudness", "speechiness", "tempo", "valence"]

start_time = time.time()
dat = pd.read_csv('output\\nprs\\track_audio_features.csv', header=0, usecols=cols)
items = pd.read_csv('output\\nprs\\mapper_item.csv', header=0)

dat_dict = {}

for index, row in dat.iterrows():
    if index % 10000 == 0:
        print(index)
    if row['track_id'] not in dat_dict:
        dat_dict[row['track_id']] = {"acousticness": row['acousticness'], "danceability": row["danceability"],
                                     "energy": row["energy"], "instrumentalness": row["instrumentalness"], "key":
                                         row["key"], "liveness": row["liveness"], "loudness": row["loudness"],
                                     "speechiness": row["speechiness"], "tempo": row["tempo"], "valence":
                                         row["valence"]}

all_songs = []
for col in items:
    print(f'{items[col].values[0]} - {col}')
    print(dat_dict[col])
    sd = dat_dict[col]
    song = {'id': items[col].values[0], 'nprs_id': col, 'acousticness': sd['acousticness'], 'danceability':
            sd['danceability'], 'energy': sd['energy'], 'instrumentalness': sd['instrumentalness'], 'key': sd['key'],
            'liveness': sd['liveness'], 'loudness': sd['loudness'], 'speechiness': sd['speechiness'],
            'tempo': sd['tempo'], 'valence': sd['valence']}
    all_songs.append(song)

res_df = pd.DataFrame(all_songs)
res_df.sort_values('id').to_csv('output\\nprs\\nprs_audio_features.csv', index=False)
