# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from mirakui_scrapy.spider_status_store import SpiderStatusStore

class EntryDeltaPipeline(object):
    def __init__(self):
        self.latest_entry_id = {}
        self.store = SpiderStatusStore()

    def open_spider(self, spider):
        entry_id = self.store.get(spider.name)
        self.latest_entry_id[spider.name] = entry_id

    def process_item(self, item, spider):
        if item['entry_id'] > self.latest_entry_id[spider.name]:
            self.latest_entry_id[spider.name] = item['entry_id']
            self.store.set(spider.name, item['entry_id'])
            return item
        else:
            pass