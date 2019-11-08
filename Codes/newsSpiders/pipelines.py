# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exporters import JsonLinesItemExporter
import os


class MultiJSONPipeline(object):

    def __init__(self):
        # dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        # dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        self.data_dir = os.getcwd().split('/NewsScraping/')[0] + '/NewsScraping/Data'
        self.files = None
        self.exporters = None

    def open_spider(self, spider):
        self.files = {'article': open(f'{self.data_dir}/article.jsonl', 'ab'),
                      'article_snapshot': open(f'{self.data_dir}/article_snapshot.jsonl', 'ab')}
        self.exporters = {'article': JsonLinesItemExporter(self.files['article'], export_empty_fields=False),
                          'article_snapshot': JsonLinesItemExporter(self.files['article_snapshot'], export_empty_fields=False)}
        # start exporter
        [e.start_exporting() for e in self.exporters.values()]

    def close_spider(self, spider):
        # close exporter
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        if spider.name == 'discover_new_articles':
            for key in item.keys():
                self.exporters[key].export_item(item[key])

        elif spider.name == 'update_contents':
            self.exporters['article_snapshot'].export_item(item['article_snapshot'])

            # todo: how to update article.jsonl



