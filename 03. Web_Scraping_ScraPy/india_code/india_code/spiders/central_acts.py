from pathlib import Path
import scrapy

class CentralActsSpider(scrapy.Spider):
    name="central_acts"
    start_urls = [
        "https://www.indiacode.nic.in/handle/123456789/1362/browse?page-token=1552de317077&page-token-value=0eb31a8e0107c0923155682b5424e2c7&nccharset=ABD5E664&type=ministry&order=ASC&rpp=100&submit_browse=Update"
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }
    
    def parse(self, response):
        links = response.css('.list-group-item>a::attr(href)').getall()
        categories = response.css('.list-group-item>a::text').getall()
        for link, category in zip(links, categories):
            yield response.follow(link, callback=self.parse_category, cb_kwargs={'category':category})
    
    def parse_category(self, response, category):
        view_links = response.xpath('//td[@headers="t4"]/a/@href').extract()
        for link in view_links:
            yield response.follow(link, callback=self.parse_detail, cb_kwargs={'category':category})
        next_link = response.css('a.pull-right::attr(href)').get()
        if next_link is not None:
            yield response.follow(next_link, callback=self.parse_category, cb_kwargs={'category':category})

    def parse_detail(self, response, category):
        details = response.css('.row>a::attr(href)').get()
        
        yield {
            'Category': category,
            'PDF Act': response.urljoin(details)
        }