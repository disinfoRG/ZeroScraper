# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import os
import jsonlines


class MultiJSONPipeline(object):

    def __init__(self):
        # dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        # dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        self.data_dir = os.getcwd().split('/NewsScraping/')[0] + '/NewsScraping/Data'
        try:
            self.existing_urls = [obj['url'] for obj in jsonlines.open(f'{self.data_dir}/article.jl')]
        except FileNotFoundError:
            self.existing_urls = list()
        self.files = None
        self.exporters = None

    def open_spider(self, spider):
        self.files = {'article': open(f'{self.data_dir}/article.jl', 'ab'),
                      'article_snapshot': open(f'{self.data_dir}/article_snapshot.jl', 'ab')}
        self.exporters = {'article': JsonLinesItemExporter(self.files['article'],
                                                           fields_to_export=['article_id', 'site_id', 'url', 'found_at',
                                                                             'last_fetched_at', 'redirect_from'],
                                                           export_empty_fields=False),
                          'article_snapshot': JsonLinesItemExporter(self.files['article_snapshot'],
                                                                    fields_to_export=['article_id', 'fetched_at', 'raw_body'],
                                                                    export_empty_fields=False)}
        # start exporter
        [e.start_exporting() for e in self.exporters.values()]

    def close_spider(self, spider):
        # finish exporter
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        # todo: more efficient way of checking?
        if item['url'] in self.existing_urls:
            raise DropItem("url already existed!")
        else:
            self.exporters['article_snapshot'].export_item(item)
            self.exporters['article'].export_item(item)
