#!/usr/bin/env python3

# =============================================================== #
# This file is going to build an object that utilizes the newspaper3k
# package and can be used inside the other scraper projects. I need
# to set the object to target specific elements on the sites that I
# have stored in the urls.txt file.
#
# This is where I will put together those elements and build the
# processes needed to extract all the market news I want.
#================================================================= #

from newspaper import Article
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os, sys
from scrapy.spiders import CrawlSpider


class MarketNewsSpider(CrawlSpider):
    name = 'market_news'
    allowed_domains = ['cnbc.com']
    start_urls = self.get_urls()

    def __init__(self):

        def get_urls(self, file_name:str):
            """Get the URLs from the url """
