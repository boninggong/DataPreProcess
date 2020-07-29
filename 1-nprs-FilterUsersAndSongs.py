import pandas as pd
pd.set_option('display.max_columns', None)

# Reads the original #NowPlaying-RS data and filters it to keep only users with more than 3000 interactions and
# songs that have been interacted with at least 200 times. After all the pre-processing this will result in a
# subset existing of 333 users, 7304 songs and 108,202 interactions.
df = pd.read_csv('data\\nprs\\context_content_features.csv', header=0)
df = df[df['user_id'].isin(df['user_id'].value_counts()[df['user_id'].value_counts() > 3000].index)]
df = df[df['track_id'].isin(df['track_id'].value_counts()[df['track_id'].value_counts() >= 200].index)]

df.to_csv('output\\nprs\\listening_events.csv', index=False)
