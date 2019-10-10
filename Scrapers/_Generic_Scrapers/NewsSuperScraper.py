import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os


class NewsSuperScraper:

    def __init__(self, primary_url, site_name, site_id):
        self.header = {'User-agent': 'Googlebot'}
        self.primary_url = primary_url
        self.site_name = site_name
        self.site_id = site_id
        self.datetime = datetime.utcnow() + timedelta(hours=8)
        self.date = self.datetime.strftime('%Y-%m-%d')
        self.time = self.datetime.strftime('%H:%M:%S')
        self.start = datetime.utcnow()
        self.news_catalog = None
        self.catalog_csv_path = f'../Data/Catalogs/{self.site_id}.csv'
        self.article_directory_savepath = f'../Data/Articles/{self.site_id}'
        self.max_page = 100

        print('********** SCRAPE INFORMATION **********\n')
        print('Today\'s Date:\t' + str(self.date))
        print('Current Time:\t' + str(self.time))
        print(f'News Website: {site_id}-{site_name}')
        print(f'News Website url: {self.primary_url}')
        print('\n****************************************\n')
        print('Executing scrape...')

        if not os.path.exists(self.article_directory_savepath):
            print('Creating directory to store articles...')
            os.makedirs(self.article_directory_savepath)

        if os.path.exists(self.catalog_csv_path):
            df = pd.read_csv(self.catalog_csv_path, usecols=['News_Date'])
            previous_dates = np.unique(df)
            previous_date_obj = [datetime.strptime(x, "%Y-%m-%d") for x in previous_dates]
            self.last_news_date_obj = max(previous_date_obj)
            print(f'Previously stopped at date = {datetime.strftime(self.last_news_date_obj, "%Y-%m-%d")}')

        else:
            print('First Time Scraping...')
            self.last_news_date_obj = datetime.min

    def collect_news_url_and_meta(self):
        return dict()

    def save_catalog(self):
        print('\n Saving Catalog...')

        def assign_news_index(group):
            group['id'] = range(1, len(group['News_URL']) + 1)
            return group

        new_df = pd.DataFrame.from_dict(self.news_catalog)
        new_df = new_df.groupby('News_Date').apply(assign_news_index)
        new_df['News_ID'] = new_df.apply(lambda x: x['News_Date'] + '-' + str(x['id']), axis=1)
        new_df = new_df.drop('id', axis=1)
        self.news_catalog = new_df.to_dict('series')
        columns = list(new_df.columns)

        # format
        new_df['Scrape_Date'] = self.date
        new_df['Site_Name'] = self.site_name
        new_df['Site_ID'] = self.site_id
        new_df = new_df[['Scrape_Date', 'Site_Name', 'Site_ID'] + columns]
        # save new catalog csv if none exist or append to previous catalog
        # TODO: test code
        if os.path.exists(self.catalog_csv_path):
            new_df.to_csv(self.catalog_csv_path, mode='a', header=False, index=False)
        else:
            new_df.to_csv(self.catalog_csv_path, mode='w', index=False)

    def collect_and_save_news_articles(self):
        pass

    def run(self):
        self.news_catalog = self.collect_news_url_and_meta()
        if self.news_catalog:
            self.save_catalog()
            self.collect_and_save_news_articles()
        else:
            print('No new articles since last time...')
        stop = datetime.utcnow()
        elapsed = stop - self.start
        print('Total Time:', elapsed)
        print('\n****************************************')
