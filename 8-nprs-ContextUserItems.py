import pandas as pd
import csv

# Creates multiple summarizing files that serve as pre-processing data
# These will be used by the Re-RankSystem and will save significant processing time
AUDIO_FEATURES = ["acousticness", "danceability", "energy", "instrumentalness", "key", "liveness", "loudness",
                  "speechiness", "tempo", "valence"]
pos_rating_weights = [1, 1, 1]
songs_ignore = [38, 5837]  # Use the id of corrupt audio feature songs gathered from step 6


# Creates a new data file where ratings are ordered per contextual condition per user
def create_context_file(v):
    ratings = pd.read_csv('output\\nprs\\nowplaying-rs-final.csv', delimiter=',')
    all_context_conditions = {}
    user_context_ratings = {}

    for i, row in ratings.iterrows():
        if row['UserID'] not in user_context_ratings:
            user_context_ratings[row['UserID']] = {}
        if row['Condition'] not in all_context_conditions:
            all_context_conditions[row['Condition']] = 0

    for context in all_context_conditions:
        for user in user_context_ratings:
            user_context_ratings[user][context] = ''

    for i, row in ratings.iterrows():
        user_context_ratings[row['UserID']][row['Condition']] = user_context_ratings[row['UserID']][row['Condition']] + \
                                                                f'({row["ItemID"]},{row["Rating"]});'

    header = ["User", "Context", "Item_Rating_Pair"]

    with open("output\\nprs\\user_context_items.csv", "w", newline="") as f:
        w = csv.DictWriter(f, header)
        w.writeheader()
        for user, v in user_context_ratings.items():
            for contextual_condition, item_rating_pair in user_context_ratings[user].items():
                row = {}
                row['User'] = user
                row['Context'] = contextual_condition
                row['Item_Rating_Pair'] = item_rating_pair[:-1]
                w.writerow(row)


def afs_sums_multiple_songs(song_rating):
    all_feat = {"acousticness": [], "danceability": [], "energy": [], "instrumentalness": [], "key": [],
                "liveness": [], "loudness": [], "speechiness": [], "tempo": [], "valence": []}
    feat_sums = {}
    sum_used_ratings = 0
    unused_items = 0
    total_used = 0

    for (song_id, rating) in song_rating:
        if song_id not in songs_ignore:
            total_used = total_used + 1
            row = songs.loc[songs['id'] == song_id]
            weight = pos_rating_weights[0]
            if rating == 4:
                weight = pos_rating_weights[1]
            elif rating == 5:
                weight = pos_rating_weights[2]
            sum_used_ratings = sum_used_ratings + weight
            for af in AUDIO_FEATURES:
                all_feat[af].append(weight * row[af].item())
        else:
            unused_items = unused_items + 1

    for af in all_feat:
        feat_sum = sum(all_feat[af])
        feat_sums[af] = feat_sum

    feat_sums['total'] = total_used

    return feat_sums


create_context_file()

user_cntxs = pd.read_csv('output\\nprs\\user_context_items.csv', delimiter=',')
songs = pd.read_csv('output\\nprs\\nprs_audio_features.csv', delimiter=',')

res_dict = {'User': [], 'Context': [], 'Amount': [], "acousticness": [], "danceability": [], "energy": [],
            "instrumentalness": [], "key": [], "liveness": [], "loudness": [], "speechiness": [], "tempo": [],
            "valence": []}
for index, row in user_cntxs.iterrows():
    print(row['User'])
    res_dict['User'].append(row['User'])
    res_dict['Context'].append(row['Context'])

    if isinstance(row['Item_Rating_Pair'], str):
        all_user_ratings = row['Item_Rating_Pair'].split(';')
        all_user_ratings = [eval(x) for x in all_user_ratings]

        feat_sums = afs_sums_multiple_songs(all_user_ratings)
        res_dict['Amount'].append(feat_sums['total'])
        for af in AUDIO_FEATURES:
            res_dict[af].append(feat_sums[af])
    else:
        res_dict['Amount'].append(0)
        for af in AUDIO_FEATURES:
            res_dict[af].append(0)

res_df = pd.DataFrame(res_dict)
res_df.to_csv('output\\nprs\\user_context_sums.csv', index=False, float_format='%.5f')
