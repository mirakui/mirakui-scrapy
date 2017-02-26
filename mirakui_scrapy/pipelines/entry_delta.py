# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from mirakui_scrapy.spider_status_store import SpiderStatusStore

class EntryDeltaPipeline(object):
    def __init__(self, store):
        self.latest_entry_id = {}
        self.store = store

    @classmethod
    def from_crawler(cls, crawler):
        store = SpiderStatusStore(
            table_name=crawler.settings.get('SPIDER_STATUS_STORE_TABLE_NAME'),
            aws_access_key_id=crawler.settings.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=crawler.settings.get('AWS_SECRET_ACCESS_KEY'),
        )
        return cls(store=store)

    def open_spider(self, spider):
        entry_id = self.store.get(spider.name)
        self.latest_entry_id[spider.name] = entry_id

    def process_item(self, item, spider):
        if item['id'] > self.latest_entry_id[spider.name]:
            if not spider.settings.getbool('DONT_UPDATE_ENTRY_DELTA'):
                self.latest_entry_id[spider.name] = item['id']
                self.store.set(spider.name, item['id'])
            return item
        else:
            raise scrapy.exceptions.DropItem
