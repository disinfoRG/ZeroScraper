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


primary_url = 'http://www.qiqi.world/'
site_name = '琦琦看新聞'
site_id = 'N3'
target_dates = None


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

    def collect_all_news_url_and_meta(self, max_page):
        # init
        all_news_urls = []
        all_news_titles = []
        all_news_dates = []
        all_news_categories = []

        next_page_url = primary_url
        page_count = 1
        while next_page_url and page_count <= max_page:
            sys.stdout.write(f'\r - Now on page {str(page_count).zfill(2)}')
            news_urls, news_titles, news_dates, news_categories = self.collect_news_url_and_meta_from_single_page(next_page_url)
            all_news_urls += news_urls
            all_news_categories += news_categories
            all_news_dates += news_dates
            all_news_titles += news_titles

            try:
                partial_next_page_url = self.soup.find('li', {'class': 'next'}).find('a')['href']
                next_page_url = urljoin(primary_url, partial_next_page_url)
                page_count += 1
            except TypeError:
                next_page_url = None
                print('\n Reach Last Page... Done.')
            time.sleep(uniform(3, 5))
            if page_count > max_page:
                print('\n Reach Max Page... Done.')

        news_info = {'News_URL': all_news_urls,
                     'News_Title': all_news_titles,
                     'News_Date': all_news_dates,
                     'News_Category': all_news_categories}
        return news_info

    def collect_target_date_news_url_and_meta(self):
        # init
        all_news_urls = []
        all_news_titles = []
        all_news_dates = []
        all_news_categories = []
        target_date_news_catalog = dict()
        # init
        next_page_url = self.primary_url
        finish = False
        while not finish:
            news_urls, news_titles, news_dates, news_categories = self.collect_news_url_and_meta_from_single_page(next_page_url)
            news_dates_obj = [datetime.strptime(x, "%Y-%m-%d") for x in news_dates]
            target_date_news_index = [i for i, date in enumerate(news_dates_obj) if date > self.last_news_date_obj]
            if len(target_date_news_index) == 0:
                break
            else:
                all_news_urls += [news_urls[j] for j in target_date_news_index]
                all_news_categories += [news_categories[j] for j in target_date_news_index]
                all_news_dates += [news_dates[j] for j in target_date_news_index]
                all_news_titles += [news_titles[j] for j in target_date_news_index]
                partial_next_page_url = self.soup.find('li', {'class': 'next'}).find('a')['href']
                next_page_url = urljoin(primary_url, partial_next_page_url)

        if all_news_urls:
            target_date_news_catalog['News_URL'] = all_news_urls
            target_date_news_catalog['News_Date'] = all_news_dates
            target_date_news_catalog['News_Title'] = all_news_titles
            target_date_news_catalog['News_Category'] = all_news_categories

        return target_date_news_catalog

    def create_catalog_dict(self):
        print('Collecting news urls and meta data ... ')
        if not os.path.exists(self.catalog_csv_path):
            self.news_catalog = self.collect_all_news_url_and_meta(max_page=100)
        else:
            self.news_catalog = self.collect_target_date_news_url_and_meta()

    def collect_and_save_news_articles(self):
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


scraper = QiqiScraper(primary_url, site_name, site_id, target_dates)
scraper.run()




