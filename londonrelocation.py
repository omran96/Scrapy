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
            property.add_value('title', titles[x].strip())
            property.add_value('price', prices[x].strip('\u00a3'))
            property.add_value('url', 'https://londonrelocation.com'+urls[x])
            yield property.load_item()
        next_page= response.xpath('/html/body/section/div/div[12]/div/ul/li[3]/a/@href').extract()
        if next_page:
            next_page = response.xpath('/html/body/section/div/div[12]/div/ul/li[3]/a/@href').extract()[0]
            next_page=response.urljoin(next_page)
            yield Request(url=next_page, callback=self.parse_area_pages)




