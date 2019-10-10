import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from random import uniform
import sys
import re
from datetime import datetime
import os
from _Generic_Scrapers.NewsSuperScraper import NewsSuperScraper
import pandas as pd

primary_url = 'http://www.cnba.live/'
site_name = '琦琦看新聞'
site_id = 'N6'


class QiqiScraper(NewsSuperScraper):
    def collect_news_url_and_meta_from_single_page(self, page_url):
        r = requests.get(page_url, headers=self.header)
        soup = BeautifulSoup(r.text, 'html5lib')
        self.soup = soup
        news_urls = [urljoin(primary_url, x['href']) for x in soup.find_all('a', href=lambda href: 'show' in href)][0::2]
        news_titles = [x.text for x in soup.find_all('a', href=lambda href: 'show' in href)]
        news_titles = list(filter(bool, news_titles))
        news_dates = [x.find('a').next_sibling.strip() for x in soup.find_all('div', {'class': 'meta'})]
        news_dates = [re.sub('[^0-9]', '-', x).strip('-') for x in news_dates]
        news_categories = [x.find('a').text.strip() for x in soup.find_all('div', {'class': 'meta'})]
        return news_urls, news_titles, news_dates, news_categories

    def collect_news_url_and_meta(self):
        # init
        all_news_urls = []
        all_news_titles = []
        all_news_dates = []
        all_news_categories = []
        target_date_news_catalog = dict()
        next_page_url = self.primary_url
        finish = False
        p = 1
        while not finish:
            sys.stdout.write(f'\r {str(p).zfill(3)}, url = {next_page_url}')
            news_urls, news_titles, news_dates, news_categories = self.collect_news_url_and_meta_from_single_page(next_page_url)
            time.sleep(uniform(2, 4))
            news_dates_obj = [datetime.strptime(x, "%Y-%m-%d") for x in news_dates]
            target_date_news_index = [i for i, date in enumerate(news_dates_obj) if date > self.last_news_date_obj]
            if len(target_date_news_index) == 0:
                break
            else:
                all_news_urls += [news_urls[j] for j in target_date_news_index]
                all_news_categories += [news_categories[j] for j in target_date_news_index]
                all_news_dates += [news_dates[j] for j in target_date_news_index]
                all_news_titles += [news_titles[j] for j in target_date_news_index]
                try:
                    partial_next_page_url = self.soup.find('li', {'class': 'next'}).find('a')['href']
                    next_page_url = urljoin(primary_url, partial_next_page_url)
                except TypeError:
                    finish = True
                    print('\n Reach Last Page... Done.')
                if p >= self.max_page:
                    finish = True
                    print('\n Reach Max Page... Done.')
                p += 1

        target_date_news_catalog['News_URL'] = all_news_urls
        target_date_news_catalog['News_Date'] = all_news_dates
        target_date_news_catalog['News_Title'] = all_news_titles
        target_date_news_catalog['News_Category'] = all_news_categories
        return target_date_news_catalog

    def collect_and_save_news_articles(self):
        df = pd.read_csv('../Data/Catalogs/N6.csv')
        self.news_catalog = df.to_dict('series')
        all_news_urls = self.news_catalog['News_URL']
        all_news_ids = self.news_catalog['News_ID']
        print(f'\nCollecting {len(all_news_urls)} news articles....')
        for i in range(len(all_news_urls)):
            url = all_news_urls[i]
            news_id = all_news_ids[i]
            sys.stdout.write(f'\r {str(i+1).zfill(4)}, url = {url}')
            if os.path.exists(os.path.join(self.article_directory_savepath, news_id) + ".txt"):
                continue
            r = requests.get(url, headers=self.header)
            time.sleep(uniform(2, 4))
            soup = BeautifulSoup(r.text, 'html5lib')
            article = ' '.join([x.text for x in soup.find_all('p')])
            with open(os.path.join(self.article_directory_savepath, news_id)+".txt", "w") as text_file:
                text_file.write(article)


scraper = QiqiScraper(primary_url, site_name, site_id)
scraper.run()




