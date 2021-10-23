import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
# from property import Property
from itemloaders.processors import Join


class Property(scrapy.Item):
    title = scrapy.Field(output_processor=Join())
    price = scrapy.Field(output_processor=Join())
    url = scrapy.Field(output_processor=Join())



class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            print(area_url)
            yield Request(url=area_url,callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        titles = response.xpath('.//div[contains(@class,"container")]//h4/a/text()').extract()
        urls=response.xpath('.//div[contains(@class,"container")]//h4/a/@href').extract()
        prices =response.xpath('.//div[contains(@class,"container")]//h5/text()').extract()
        for x in range(len(prices)):
            property = ItemLoader(item=Property())
            property.add_value('title', titles[x])
            property.add_value('price', prices[x])
            property.add_value('url', 'https://londonrelocation.com'+urls[x])
            return property.load_item()


