from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import sys
import linecache


class NewsSuperScraper:

    def __init__(self, site_url, site_name, site_id):
        self.header = {'User-agent': 'Googlebot'}
        self.site_url = site_url
        self.site_name = site_name
        self.site_id = site_id
        self.start = datetime.utcnow() + timedelta(hours=8)
        print('********** SCRAPE INFORMATION **********\n')
        print('Today\'s Date:\t' + str(self.start.strftime('%Y-%m-%d')))
        print('Current Time:\t' + str(self.start.strftime('%H:%M:%S')))
        print(f'News Website: {site_id}-{site_name}')
        print(f'News Website url: {self.site_url}')
        print('\n****************************************\n')
        print('Executing scrape...')

        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if not self.es.exists(index='sites', id=self.site_id):
            self.es.create(index='sites', id=self.site_id, body={'url': self.site_url, 'name': self.site_name})

    def collect_news_url_and_meta(self):
        return dict()

    def extract_news_content(self, url):
        html = ''
        article = ''
        images = list()
        return html, article, images

    def _generate_news_and_images_documents(self):
        # generate data
        news_count = len(self.all_news_metadata)
        news_documents = []
        images_documents = []
        current_time = datetime.utcnow() + timedelta(hours=8)
        print(f' Bulk saving {news_count} news...')
        for i in range(news_count):
            news = self.all_news_metadata[i]
            sys.stdout.write(f'\r {str(i+1).zfill(4)}, url = {news["url"]}')
            news['html'], news['content'], news['content_images'] = self.extract_news_content(news['url'])
            images_documents.append({'_index': 'images', '_id': news['front_img_url'],
                                     'string': news['front_img_string'],
                                     'type': 'front', 'news_id': news['url'], 'scrape_datetime': current_time})
            images_documents += [{'_index': 'images', **images, 'news_id': news['url'], 'scrape_datetime': current_time}
                                 for images in news['content_images']]
            news.pop('front_img_url')
            news.pop('front_img_string')
            news.pop('content_images')
            site_level_info = {'site_id': self.site_id, 'site_name': self.site_name}
            news_documents.append({"_index": "news", "_id": news['url'],
                                   'scrape_datetime': current_time,
                                   **site_level_info, **news})

        return news_documents, images_documents

    def run(self):
        try:
            self.all_news_metadata = self.collect_news_url_and_meta()
            news_documents, images_documents = self._generate_news_and_images_documents()
            bulk(self.es, news_documents)
            bulk(self.es, images_documents)
        except:
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

        else:
            stop = datetime.utcnow() + timedelta(hours=8)
            elapsed = stop - self.start
            print('\nTotal Time:', elapsed)
            print('\n****************************************')
