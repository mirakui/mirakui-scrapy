# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from mirakui_scrapy.dynamodb import DynamoDB

class MirakuiScrapyPipeline(object):
    def __init__(self):
        self.latest_entry_id = {}
        self.db = DynamoDB()

    def open_spider(self, spider):
        entry_id = self.db.get(spider.name)
        self.latest_entry_id[spider.name] = entry_id

    def process_item(self, item, spider):
        if item['entry_id'] > self.latest_entry_id[spider.name]:
            self.latest_entry_id[spider.name] = item['entry_id']
            self.db.set(spider.name, item['entry_id'])
            return item
        else:
            pass
