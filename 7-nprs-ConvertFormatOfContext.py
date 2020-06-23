import pandas as pd
pd.set_option('display.max_columns', None)

ratings = pd.read_csv('output\\nprs\\nowplaying-rs-final.csv', header=0)

ratings.drop('Dimension', axis=1, inplace=True)
ratings.columns = ['UserID', 'ItemID', 'Rating', 'daytime']

ratings.to_csv('output\\nprs\\nprs_ratings.csv', index=False)
