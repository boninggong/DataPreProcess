import pandas as pd

# Extracts useful columns within the dataset and splits it to 2 separate files
df = pd.read_csv('output\\nprs\\listening_events.csv', header=0)

new_df = df[['user_id', 'track_id', 'created_at', 'time_zone']].copy()
new_df.to_csv('output\\nprs\\user_track.csv', index=False)

audio_df = df[['track_id', 'instrumentalness', 'liveness', 'speechiness', 'danceability', 'valence', 'loudness',
               'tempo', 'acousticness', 'energy', 'key']].copy()
audio_df.to_csv('output\\nprs\\track_audio_features.csv', index=False)
