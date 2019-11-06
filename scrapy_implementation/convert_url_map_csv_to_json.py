import json
import pandas as pd
import sys

file_path = 'url_map.csv'
url_map_df = pd.read_csv(file_path)
url_map_df = url_map_df.set_index('id')
url_map_df.to_json('url_map.json', orient='index')

# read
# json.load(open('url_map.json', 'r'))