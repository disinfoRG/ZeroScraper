import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from random import uniform
import sys
import re
from NewsSuperScraper import NewsSuperScraper
import base64


class QiqiScraper(NewsSuperScraper):
    def __init__(self, site_url, site_name, site_id):
        super().__init__(site_url, site_name, site_id)
        self.max_page = 10

    def collect_news_url_and_meta_from_single_page(self, soup):
        news_urls = [urljoin(self.site_url, x['href']) for x in soup.find_all('a', href=lambda href: 'show' in href)][0::2]
        news_titles = [x.text for x in soup.find_all('a', href=lambda href: 'show' in href)]
        news_titles = list(filter(bool, news_titles))
        news_dates = [x.find('a').next_sibling.strip() for x in soup.find_all('div', {'class': 'meta'})]
        news_dates = [re.sub('[^0-9]', '-', x).strip('-') for x in news_dates]
        news_categories = [x.find('a').text.strip() for x in soup.find_all('div', {'class': 'meta'})]
        news_front_image_urls = [self.site_url+x.find('img')['src'] for x in soup.find_all('div', {'class': 'media-left'})]
        news_front_image_strings = [base64.b64encode(requests.get(img_url).content).decode('ASCII')
                                    for img_url in news_front_image_urls]
        news_metadata = []
        for data in zip(news_urls, news_titles, news_dates, news_categories, news_front_image_urls,
                        news_front_image_strings):
            news_metadata.append(dict(zip(('url', 'title', 'date', 'category', 'front_img_url', 'front_img_string'),
                                          data)))

        return news_metadata

    def collect_news_url_and_meta(self):
        # init
        all_news_metadata = []
        next_page_url = self.site_url
        finish = False
        p = 1
        while not finish:
            sys.stdout.write(f'\r {str(p).zfill(3)}, url = {next_page_url}')
            r = requests.get(next_page_url, headers=self.header)
            time.sleep(uniform(2, 4))
            soup = BeautifulSoup(r.text, 'html5lib')
            news_metadata = self.collect_news_url_and_meta_from_single_page(soup)
            all_news_metadata += news_metadata
            try:
                partial_next_page_url = soup.find('li', {'class': 'next'}).find('a')['href']
                next_page_url = urljoin(self.site_url, partial_next_page_url)
            except TypeError:
                finish = True
                print('\n Reach Last Page... Done.')
            if p >= self.max_page:
                finish = True
                print('\n Reach Max Page... Done.')
            p += 1

        return all_news_metadata

    def extract_news_content(self, url):
        r = requests.get(url, headers=self.header)
        html = r.text
        time.sleep(uniform(2, 4))
        soup = BeautifulSoup(html, 'html5lib')
        main_content = soup.select_one('div#node-content')
        article = ' '.join([x.text for x in main_content.find_all('p')])
        img_elements = main_content.select('div.figure')
        images = []
        for img_ele in img_elements:
            img_url = img_ele.img['src']
            img_str = base64.b64encode(requests.get(img_url).content).decode('ASCII')
            images.append({'_id': img_url, 'string': img_str, 'type': 'content'})
        return html, article, images
