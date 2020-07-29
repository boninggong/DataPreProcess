import pandas as pd
from datetime import datetime
from datetime import timedelta

# Converts time of tweets to the users' local time zones and groups them together
df = pd.read_csv('output\\nprs\\user_track.csv', header=0)
res_dict = {'UserID': [], 'ItemID': [], 'Rating': 1, 'Dimension': 'DayTime', 'Condition': []}

for index, row in df.iterrows():
    time = datetime.strptime(row['created_at'], "%Y-%m-%d %H:%M:%S")

    if isinstance(row['time_zone'], str):

        res_dict['UserID'].append(row['user_id'])
        res_dict['ItemID'].append(row['track_id'])

        if 'Pacific' in row['time_zone']:
            time = time - timedelta(hours=8)
        elif 'Eastern' in row['time_zone']:
            time = time - timedelta(hours=5)
        elif 'Central' in row['time_zone']:
            time = time - timedelta(hours=6)
        elif 'Beijing' in row['time_zone']:
            time = time + timedelta(hours=8)
        elif 'Berlin' in row['time_zone']:
            time = time + timedelta(hours=8)

        if 6 <= time.hour < 12:
            day_time = 'morning'
        elif 12 <= time.hour < 18:
            day_time = 'afternoon'
        elif 18 <= time.hour < 24:
            day_time = 'evening'
        elif 0 <= time.hour < 6:
            day_time = 'night'

        res_dict['Condition'].append(day_time)

res_df = pd.DataFrame(res_dict)

print(f'Total ratings: {res_df.shape[0]}')
print()
print(f'Users: {len(res_df.UserID.unique())}')
print()
print(f'Items: {len(res_df.ItemID.unique())}')

res_df.to_csv('output\\nprs\\nowplaying-rs.csv', index=False)
