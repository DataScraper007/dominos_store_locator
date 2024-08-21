import gzip
import scrapy
from scrapy.cmdline import execute
from dominos.items import DominosItem
import random


class LocationScraperSpider(scrapy.Spider):
    name = "location_scraper"
    allowed_domains = ['stores.dominos.co.in']
    start_urls = ["https://stores.dominos.co.in"]

    def parse(self, response, **kwargs):

        # Generate a random 4-digit number
        random_number = random.randint(1000, 9999)
        # Page save
        # with gzip.open(rf'C:\Users\Admin\PycharmProjects\page_save\dominos\{random_number}.html.gz', 'wb') as page:
        #     page.write(response.body)
        # print('Page saved...')
        item = DominosItem()

        # Extract the list of containers holding store details
        containers = response.xpath('//ul[contains(@class,"outlet-detail")]')

        # Iterate over each container to extract store information
        for container in containers:
            # Extract and clean the store name
            item['name'] = container.xpath('./li[@class="outlet-name"]//a/text()').get().strip()

            # Extract the landmark
            landmark = container.xpath('./li[not(@class)]/div[@class="info-text"]/text()').getall()

            # Set the landmark field if available, otherwise default to 'N/A'
            if len(landmark) > 1:
                item['landmark'] = landmark[1].strip()
            else:
                item['landmark'] = 'N/A'

            # Construct address components from address string
            address = container.xpath('./li[@class="outlet-address"]/div[@class="info-text"]//span/text()').getall()
            item['address'] = address[0] + address[1]
            item['city'] = address[2]
            item['pincode'] = address[4]

            # Extract and clean the phone number
            item['phone'] = container.xpath(
                './li[@class="outlet-phone"]/div[@class="info-text"]/a/text()').get().strip()

            # Extract the map URL and website URL
            item['map_url'] = container.xpath('./li[@class="outlet-actions"]/a[@class="btn btn-map"]/@href').get()
            item['website'] = container.xpath('./li[@class="outlet-actions"]/a[@class="btn btn-website"]/@href').get()

            # Extract the store timings and parse the closing time
            timings = container.xpath('./li[@class="outlet-timings"]/div[@class="info-text"]/span/text()').get()
            if "Open until" in timings:
                item['closing_time'] = timings.replace("Open until ", '')
            else:
                item['closing_time'] = 'N/A'

            # Current page url
            item['page_url'] = response.request.url

            yield item

        # Extract the URL for the next page of results, if available
        next_page = response.xpath('//ul[@class="pagination "]/li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)


# Execute the spider from the command line
if __name__ == '__main__':
    execute('scrapy crawl location_scraper'.split())
