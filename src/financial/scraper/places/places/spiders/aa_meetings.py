import scrapy
from ..items import MeetingItem
from bs4 import BeautifulSoup as bs
import pandas as pd
import lxml


class AaMeetingsSpider(scrapy.Spider):
    name = 'aa_meetings'
    allowed_domains = ['www.aa-meetings.com']
    start_urls = ['https://www.aa-meetings.com/aa-meeting/']
    base_url = 'https://www.aa-meetings.com/aa-meeting'

    def start_requests(self):
        urls = self.start_urls
        for url in urls:
            response = scrapy.Request(url=url, callback=self.parse)
            yield response
        for num in range(2, 2800):
            url = self.base_url + '/page/' + str(num) + '/'
            response = scrapy.Request(url, callback=self.parse)
            yield response


    def parse(self, response):
        # get each meeting link on the page. The spider will have to follow
        # each link to aquire the needed information. Once the all the links
        # have been followed, the spider will have to go to the next page.
        page_links = response.xpath('//div[@class="fui-card-body"]//a/@href').getall()
        for link in page_links:
            self.logger.info('Retrieving data from %s', link)
            yield scrapy.Request(response.urljoin(link), self.parse_meeting_page)


    def parse_meeting_page(self, response):
        self.logger.info('Retrieving item data from %s', response.url)

        # meeting name:
        name = response.css('div.fui-card-body p.weight-300::text').get()

        # Get link to meeting page
        link = response.url

        # get address data:
        street = response.css('div.fui-card-body address.weight-300::text').get()

        try:
            # make sure that all of the card values are scraped and valid
            # to avoid raising a ValueError exception
            card = response.css('div.fui-card-body p.weight-300 a::text').getall()
            if len(card) == 3:
                # Get city, state and zipcode:
                city, state, zipcode = card
            elif len(card) == 2:
                city, state = card
                zipcode = 'zipcode'
            elif len(card) == 1:
                city = card
                state, zipcode = 'state', 'zipcode'
            else:
                city, state, zipcode = 'city', 'state', 'zipcode'
        except ValueError as ve:
            self.logger.error(f'{ve} Exception Raised..')

        try:
            # make sure that all of the table values are scraped and valid
            # to avoid raising a ValueError exception
            table = response.xpath('//*[@class="table fui-table"]//tr//td/text()').getall()

            if len(table) == 3:
                day, time, info = table

            elif len(table) == 2:
                day, time = table
                info = 'info'

            elif len(table) == 1:
                day = table
                time, info  = 'time', 'info'

            elif len(table) > 3:
                    # extract table data day, time and info:
                try:
                    if len(table) == 6:
                        day = ', '.join([table[0], table[3]])
                        time = ', '.join([table[1], table[4]])
                        info = ', '.join([table[2], table[5]])

                        schedule = {'day': [table[0], table[3]],
                                    'time': [table[1], table[4]],
                                    'info': [table[2], table[5]]}

                    elif len(table) == 9:
                        day = ', '.join([table[0], table[3], table[6]])
                        time = ', '.join([table[1], table[4], table[7]])
                        info = ', '.join([table[2], table[5], table[8]])

                        schedule = {'day': [table[0], table[3], table[6]],
                                    'time': [table[1], table[4], table[7]],
                                    'info': [table[2], table[5], table[8]]}

                    elif len(table) == 12:
                        day = ', '.join([table[0], table[3], table[6], table[9]])
                        time = ', '.join([table[1], table[4], table[7], table[10]])
                        info = ', '.join([table[2], table[5], table[8], table[11]])

                        schedule = {'day': [table[0], table[3], table[6], table[9]],
                                    'time': [table[1], table[4], table[7], table[10]],
                                    'info': [table[2], table[5], table[8], table[11]]}

                    elif len(table) == 15:
                        day = ', '.join([table[0], table[3], table[6], table[9], table[12]])
                        time = ', '.join([table[1], table[4], table[7], table[10], table[13]])
                        info = ', '.join([table[2], table[5], table[8], table[11], table[14]])

                        schedule = {'day': [table[0], table[3], table[6], table[9], table[12]],
                                    'time': [table[1], table[4], table[7], table[10], table[13]],
                                    'info': [table[2], table[5], table[8], table[11], table[14]]}

                except Exception as e:
                    return f"Table with value greater than 3 unpacking failed | {e} | table length {table_len} | {day} {time} {info}"

            else:
                day, time, info = 'day', 'time', 'info'

        except ValueError as ve:
            self.logger.error(f'{ve} Exception Raised..')

        item = MeetingItem(name=name, link=link, street=street, city=city, state=state, zipcode=zipcode, day=day, time=time, info=info)
        yield item
