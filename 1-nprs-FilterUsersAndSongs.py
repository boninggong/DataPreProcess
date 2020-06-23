import pandas as pd
pd.set_option('display.max_columns', None)

df = pd.read_csv('data\\nprs\\context_content_features.csv', header=0)

# Filter 3000 user ratings, 200 track ratings, after all filters:
# 7304 items, 333 users, 108202 ratings
df = df[df['user_id'].isin(df['user_id'].value_counts()[df['user_id'].value_counts() > 3000].index)]
df = df[df['track_id'].isin(df['track_id'].value_counts()[df['track_id'].value_counts() >= 200].index)]

df.to_csv('output\\nprs\\listening_events.csv', index=False)
