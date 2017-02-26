# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urljoin

from mirakui_scrapy.items import Entry


class MangaFgo2(scrapy.Spider):
    name = 'manga_fgo2'
    allowed_domains = ['www.fate-go.jp']
    start_urls = ['http://www.fate-go.jp/manga_fgo2/']

    custom_settings = {
        'SLACK_USERNAME': 'もっとマンガで分かる！Fate/Grand Order',
    }

    def parse(self, response):
        for sel in reversed(response.css('#index ul li')):
            url = urljoin(response.url, sel.css('a::attr("href")').extract_first())
            return scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        image = response.css('#contents p.comic img')
        image_url = urljoin(response.url, image.css('::attr("src")').extract_first())
        title = image.css('::attr("alt")').extract_first()
        # 'http://www.fate-go.jp/manga_fgo2/comic63.html'
        # -> '00063'
        comic_num = re.sub(r'^.+/comic(\d+)\.html$', r'\1', response.url)
        entry_id = '%05d' % int(comic_num)
        return Entry(url=response.url, title=title, image_url=image_url, id=entry_id)
