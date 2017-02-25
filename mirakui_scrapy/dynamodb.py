# -*- coding: utf-8 -*-
import boto3

class DynamoDB:
    table_name = 'scrapy_statuses'
    region = 'ap-northeast-1'

    def db(self):
        return boto3.resource('dynamodb', region_name=self.region)

    def table(self):
        return self.db().Table(self.table_name)

    def get(self, spider_name):
        result = self.table().get_item(Key={'spider': spider_name})
        if 'Item' in result:
            return result['Item']['entry_id']
        else:
            return None

    def set(self, spider_name, entry_id):
        return self.table().put_item(Item={'spider': spider_name, 'entry_id': entry_id})
