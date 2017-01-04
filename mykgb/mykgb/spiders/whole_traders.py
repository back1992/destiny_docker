# -*- coding: utf-8 -*-
import scrapy


class WholeTradersSpider(scrapy.Spider):
    name = "whole_traders"
    allowed_domains = ["www.baidu.com"]
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
