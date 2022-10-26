import newspaper
import scrapy
import os
import sys
import re
from loguru import logger


class NewsSpider(scrapy.Spider):
    name = 'news-media'

    def __init__(self):
        self.file = open('urls.txt', 'r')

    def parse(self, response, **kwargs):
        urls = [line for line in self.file]
        for url in urls:
            yield scrapy.Request(url)
