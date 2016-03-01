# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy.selector import Selector

from crawler.items import AmazonBook


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.es"]
    start_urls = (
        #'http://www.amazon.es/',
        #'http://www.amazon.es/s/ref=lp_599364031_nr_n_0?fst=as%3Aoff&rh=n%3A599364031%2Cn%3A%21599365031%2Cn%3A902675031&bbn=599365031&ie=UTF8&qid=1455998790&rnid=599365031',
        'http://www.amazon.es/s/ref=lp_902675031_pg_2?rh=n%3A599364031%2Cn%3A%21599365031%2Cn%3A902675031&page=2&ie=UTF8&qid=1456074318',

    )

    def parse(self, response):

        for book_li in response.css('li.s-result-item a.s-access-detail-page'):

            book = AmazonBook()
            logging.info(book_li.xpath('@title')[0].extract())
            logging.info(book_li.xpath('@href')[0].extract())

            book['title'] = book_li.xpath('@title')[0].extract()
            book['link'] = book_li.xpath('@href')[0].extract()
            yield book

        next_page_url = response.css('#pagn>span.pagnCur+span>a').xpath('@href')[0].extract()
        next_page_url = response.urljoin(next_page_url)

        next_page_num = response.css('#pagn>span.pagnCur+span>a').xpath('text()')[0].extract()

        if int(next_page_num) < 5:
            yield scrapy.Request(next_page_url)
