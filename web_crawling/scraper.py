import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://www.bloomberg.com/news/features/2020-02-02/vietnam-s-economy-is-being-squeezed-in-the-u-s-china-trade-war']