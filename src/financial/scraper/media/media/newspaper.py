import newspaper
import scrapy
import os, sys, re
from loguru import logger


class NewsSpider(scrapy.Spider):
    name = 'news-media'

    def __init__(self):
        self.file = open('urls.txt', 'r')

    def parse(self, response, **kwargs):
        urls = [line for line in self.file]
