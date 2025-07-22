import pandas as pd

df = pd.read_csv('location_data/area_to_scrape.csv')
df = df.filter(['state', 'Area'])

area_to_scrape_dict = {}
for state, area in df.groupby('state'):
    area_to_scrape_dict.update({state: area["Area"].to_list()})
