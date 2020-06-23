import pandas as pd
import csv

# Creates a new data file where ratings are ordered per user, per contextual condition
ratings = pd.read_csv('output\\car\\car_context_ratings.csv', delimiter=',')
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

with open("output\\car\\user_context_items.csv", "w", newline="") as f:
    w = csv.DictWriter(f, header)
    w.writeheader()
    for user, v in user_context_ratings.items():
        for contextual_condition, item_rating_pair in user_context_ratings[user].items():
            row = {'User': user, 'Context': contextual_condition, 'Item_Rating_Pair': item_rating_pair[:-1]}
            w.writerow(row)
