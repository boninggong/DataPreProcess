import pandas as pd

# Maps original user and song IDs to our custom IDs to simplify identification
df = pd.read_csv('output\\nprs\\nowplaying-rsv.csv', header=0)
df = df.drop_duplicates(subset=['UserID', 'ItemID', 'Condition'], keep='first')

i = 1
item_mapper = {}
for index, row in df.iterrows():
    if row['ItemID'] not in item_mapper:
        item_mapper[row['ItemID']] = i
        i = i + 1
    df.at[index, 'ItemID'] = item_mapper[row['ItemID']]

i = 1
user_mapper = {}
for index, row in df.iterrows():
    if row['UserID'] not in user_mapper:
        user_mapper[row['UserID']] = i
        i = i + 1
    df.at[index, 'UserID'] = user_mapper[row['UserID']]

df.to_csv('output\\nprs\\nowplaying-rs-final.csv', index=False)

user_mapper_df = pd.DataFrame(user_mapper, index=[0])
user_mapper_df.to_csv('output\\nprs\\mapper_user.csv', index=False)

item_mapper_df = pd.DataFrame(item_mapper, index=[0])
item_mapper_df.to_csv('output\\nprs\\mapper_item.csv', index=False)
