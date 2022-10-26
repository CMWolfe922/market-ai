# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MediaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsPaperItem(Item):
    title = Field()
    body = Field()
    link = Field()
    tags = Field()
