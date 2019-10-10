import requests
from bs4 import BeautifulSoup
import time
from random import uniform
import sys
import os
from datetime import datetime
from _Generic_Scrapers.NewsSuperScraper import NewsSuperScraper
import pandas as pd

primary_url = 'http://taiwan-politicalnews.com'
site_name = '鬼島狂新聞'
site_id = 'N11'


class IslandScraper(NewsSuperScraper):
    def collect_news_url_and_meta_from_single_page(self, page_url):
        r = requests.get(page_url, headers=self.header)
        soup = BeautifulSoup(r.text, 'html5lib')
        self.soup = soup
        news_urls = [x['href'] for x in soup.find_all('a', {'class': 'entry_title'})]
        news_titles = [x['title'] for x in soup.find_all('a', {'class': 'entry_title'})]
        news_dates = [x.text.split() for x in soup.find_all('div', {'class': 'post_date_circle'})]
        news_dates = ['-'.join([date[-1], date[-3], date[-4]]) for date in news_dates]
        news_categories = [x.text for x in soup.find_all('a', {'class': 'post_card_category'})]
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

        if self.last_news_date_obj == datetime.min:
            r = requests.get(self.primary_url, headers=self.header)
            soup = BeautifulSoup(r.text, 'html5lib')
            total_pages = int(soup.select('a.next.page-numbers')[0].find_previous_sibling('a').text)
            print(f'Retrieving {str(total_pages)} pages of news url and meta data')

        while not finish:
            sys.stdout.write(f'\r Now on page {str(p).zfill(3)}, url = {next_page_url}')
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
                try:
                    next_page_url = self.soup.find('a', {'class': 'next page-numbers'})['href']
                except TypeError:
                    print(' Reach Last Page... Done.')
                    break
                else:
                    p += 1
                    time.sleep(uniform(2, 4))

        target_date_news_catalog['News_URL'] = all_news_urls
        target_date_news_catalog['News_Date'] = all_news_dates
        target_date_news_catalog['News_Title'] = all_news_titles
        target_date_news_catalog['News_Category'] = all_news_categories
        return target_date_news_catalog

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
            article = ' '.join([x.text for x in soup.find('main').find_all('p')]).strip()
            with open(os.path.join(self.article_directory_savepath, news_id)+".txt", "w") as text_file:
                text_file.write(article)


scraper = IslandScraper(primary_url, site_name, site_id)
scraper.run()




