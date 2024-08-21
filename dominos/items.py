# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DominosItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    pincode = scrapy.Field()
    landmark = scrapy.Field()
    phone = scrapy.Field()
    closing_time = scrapy.Field()
    website = scrapy.Field()
    map_url = scrapy.Field()
    page_url = scrapy.Field()
