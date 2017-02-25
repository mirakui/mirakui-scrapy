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

    def parse(self, response):
        for sel in response.css('#grid-content a'):
            entry = Entry()
            entry['url'] = urljoin(self.base_url, sel.css('::attr("href")').extract_first())

            entry['title'] = sel.css('img::attr("alt")').extract_first()
            if entry['title'] == '':
                continue

            entry['image_url'] = urljoin(self.base_url, sel.css('img::attr("src")').extract_first())
            if '/img/common/sidemenu/' in entry['image_url']:
                continue

            # 'http://photo.yodobashi.com/img/home/20160125_diary.jpg'
            # -> '20160125_diary'
            entry['entry_id'] = re.sub(r'^.*/([^/]+)\.[^\.]+$', r'\1', entry['image_url'])
            yield entry
