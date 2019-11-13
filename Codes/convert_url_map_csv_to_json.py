import os
import pandas as pd

root_dir = os.getcwd().split('/NewsScraping/')[0]+'/NewsScraping'
data_dir = root_dir+'/Data'
file_path = data_dir+'/url_map.csv'
url_map_df = pd.read_csv(file_path)
url_map_df = url_map_df.set_index('id')
url_map_df.to_json(data_dir+'/url_map.json', orient='index')
