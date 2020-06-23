import pandas as pd
import math

# Reads original dataset and writes it to such a way that there is 1 rating per contextual condition and dimension
cols = ['DrivingStyle', 'landscape', 'mood', 'naturalphenomena', 'RoadType', 'sleepiness', 'trafficConditions',
        'weather']
dat = pd.read_csv('data\\car\\car.csv', delimiter=';')
print(dat.head(10))

col_names = ['UserID', 'ItemID', 'Rating', 'Dimension', 'Condition']
my_df = pd.DataFrame(columns=col_names)

for index, row in dat.iterrows():
    for c in cols:
        if isinstance(row[c], str):
            my_df = my_df.append({'UserID': row['UserID'], 'ItemID': row['ItemID'], 'Rating': row['Rating'],
                                  'Dimension': c, 'Condition': row[c]}, ignore_index=True)
            break

my_df.to_csv('output\\car\\car_context_ratings.csv', index=False)