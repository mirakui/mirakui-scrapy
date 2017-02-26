# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urljoin

from mirakui_scrapy.items import Entry


class PhotoyodobashiSpider(scrapy.Spider):
    base_url = 'http://photo.yodobashi.com/'
    name = 'photoyodobashi'
    allowed_domains = ['photo.yodobashi.com']
    start_urls = [base_url]

    custom_settings = {
        'SLACK_USERNAME': 'フォトヨドバシ',
    }

    def parse(self, response):
        for sel in reversed(response.css('#grid-content a')):
            url = urljoin(self.base_url, sel.css('::attr("href")').extract_first())

            title = sel.css('img::attr("alt")').extract_first()
            if title == '':
                continue

            image_url = urljoin(self.base_url, sel.css('img::attr("src")').extract_first())
            if '/img/common/sidemenu/' in image_url:
                continue

            # 'http://photo.yodobashi.com/img/home/20160125_diary.jpg'
            # -> '20160125_diary'
            entry_id = re.sub(r'^.*/([^/]+)\.[^\.]+$', r'\1', image_url)
            yield Entry(url=url, title=title, image_url=image_url, id=entry_id)
