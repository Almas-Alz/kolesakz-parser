import scrapy
from random import uniform
from time import sleep


class SpiderkolesaSpider(scrapy.Spider):
    name = 'spiderkolesa'
    allowed_domains = ['kolesa.kz']
    start_urls = ['https://kolesa.kz/cars/']

    def parse(self, response):
        for i in range(1, 1000):
            url = f'https://kolesa.kz/cars/?page={i}'
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        for href in response.css(".ddl_product_link::attr('href')"):
            url = response.urljoin(href.extract())
            sleep(round(uniform(0.2, 0.4), 3))
            yield scrapy.Request(url, callback=self.parse_contents)

    def parse_contents(self, response):
        item = dict()
        item['manufacturer'] = response.css('h1 span::text').get().strip()
        item['model'] = response.css('h1 span::text').getall()[1].strip()
        item['year'] = response.css('.year::text').get().strip()
        item['city'] = response.css('dl:nth-child(1) .value::text').get().strip()
        item['body'] = response.css('dl:nth-child(2) .value::text').get().strip()
        item['engine_volume'] = response.css('dl:nth-child(3) .value::text').get().strip()
        item['mileage'] = response.css('dl:nth-child(4) .value::text').get().strip()
        item['transmission'] = response.css('dl:nth-child(5) .value::text').get().strip()
        item['wheel'] = response.css('dl:nth-child(6) .value::text').get().strip()
        item['color'] = response.css('dl:nth-child(7) .value::text').get().strip()
        item['drive'] = response.css('dl:nth-child(8) .value::text').get().strip()
        item['price'] = response.css('.offer__price::text').get().strip()
        yield item
