# -*- coding: utf-8 -*-
import boto3

class SpiderStatusStore:

    def __init__(self, table_name, aws_access_key_id, aws_secret_access_key, aws_region='ap-northeast-1'):
        self.table_name = table_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region

    def db(self):
        return boto3.resource(
            'dynamodb',
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

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
