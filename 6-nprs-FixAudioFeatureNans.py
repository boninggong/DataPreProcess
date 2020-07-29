import pandas as pd

# Min-max normalize the audio features "loudness" and "tempo"
# Checks which songs do not have complete audio features, these will be removed in step 8
# (Songs like f3b434d15747984415c37dbe236007fa and 33607ee02342c55a0c3221861d639b19)
AUDIO_FEATURES = ["acousticness", "danceability", "energy", "instrumentalness", "key", "liveness", "loudness",
                  "speechiness", "tempo", "valence"]
items = pd.read_csv('output\\nprs\\nprs_audio_features.csv', header=0)
items_with_nan = items[items.isna().any(axis=1)]
print(items_with_nan)  # Use these indices as input for step 8

items['loudness'] = items['loudness'].apply(lambda x: (x + 40)/40)
items['tempo'] = items['tempo'].apply(lambda x: x / 220)

for af in AUDIO_FEATURES:
    items[af] = items[af].apply(lambda x: round(x, 4))

items.to_csv('output\\nprs\\nprs_audio_features.csv', index=False)
