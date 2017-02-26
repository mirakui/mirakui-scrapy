import os
import requests
import json

class SlackNotifierPipeline:

    def process_item(self, item, spider):
        default_webhook_url = spider.settings['SLACK_WEBHOOK']
        webhook_url = self.__get_setting(spider, 'WEBHOOK', default_webhook_url)

        slack_data = {}
        slack_data['text'] = '%s\n%s' % (item['title'], item['url'])

        if item['image_url']:
            slack_data['attachments'] = [
                {'image_url': item['image_url']},
            ]

        username = self.__get_setting(spider, 'USERNAME')
        if username:
            slack_data['username'] = username

        channel = self.__get_setting(spider, 'SLACK_CHANNEL')
        if channel:
            slack_data['channel'] = channel

        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
        return item

    def __get_setting(self, spider, suffix, default_value=None):
        value = spider.settings['SCRAPY_SLACK_%s_%s' % (spider.name.upper(), suffix)]
        if value:
            return value
        else:
            return default_value
