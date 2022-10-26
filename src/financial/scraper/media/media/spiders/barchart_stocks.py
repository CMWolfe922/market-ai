import scrapy


class BarchartStocksSpider(scrapy.Spider):
    name = 'barchart-stocks'
    allowed_domains = ['www.barchart.com']
    start_urls = ['http://www.barchart.com/stocks/']

    def parse(self, response):
        pass
