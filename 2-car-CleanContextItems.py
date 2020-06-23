import pandas as pd
import csv

# Creates a new data file where all positive ratings (> 3) are stored per contextual condition
ratings = pd.read_csv('output\\car\\car_context_ratings.csv', delimiter=',')
contextual_values = {}

for i, row in ratings.iterrows():
    if row['Condition'] not in contextual_values:
        contextual_values[row['Condition']] = ''
    if row["Rating"] >= 4:
        contextual_values[row['Condition']] = contextual_values[row['Condition']] + f'({row["ItemID"]},{row["Rating"]});'

header = ["Context", "Item_Rating_Pair"]

with open("output\\car\\context_items_rated_positive.csv", "w", newline="") as f:
    w = csv.DictWriter(f, header)
    w.writeheader()
    for k, v in contextual_values.items():
        row = {}
        row['Context'] = k
        row['Item_Rating_Pair'] = v[:-1]
        w.writerow(row)
