from pathlib import Path
import scrapy
import csv

class StateActsSpider(scrapy.Spider):
    name="state_acts"
    start_urls=[
        "https://www.indiacode.nic.in/"
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    def parse(self, response):
        state_info = response.xpath('//a[contains(text(), "State Acts")]/following-sibling::div//li/a')
        with open('./data/state_acts.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Year', 'State', 'PDF Act']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        for state in state_info:
            name = state.xpath('normalize-space(text())').extract_first()
            url = state.xpath('@href').extract_first()
            yield response.follow(url, callback=self.parse_state_menu, cb_kwargs={'state':name})
    
    def parse_state_menu(self, response, state):
        menu_item = response.xpath('//a[contains(text(), "Act Year")]/@href').extract_first()
        yield response.follow(menu_item, callback=self.parse_state_years, cb_kwargs={'state':state})
    
    def parse_state_years(self, response, state):
        act_year_urls = response.xpath('//li[@class="list-group-item"]/a/@href').extract()
        act_years = response.xpath('//li[@class="list-group-item"]/a/text()').extract()
        for act_url, act_year in zip(act_year_urls, act_years):
            yield response.follow(act_url, callback=self.parse_state_acts, cb_kwargs={'state':state, 'year':act_year})
        next_link = response.css('a.pull-right::attr(href)').get()
        if next_link is not None:
            yield response.follow(next_link, callback=self.parse_state_years, cb_kwargs={'state':state})

    def parse_state_acts(self, response, state, year):
        view_links = response.xpath('//td[@headers="t4"]/a/@href').extract()
        for link in view_links:
            yield response.follow(link, callback=self.parse_detail, cb_kwargs={'state':state, 'year':year})
        next_link = response.css('a.pull-right::attr(href)').get()
        if next_link is not None:
            yield response.follow(next_link, callback=self.parse_state_acts, cb_kwargs={'state':state, 'year':year})

    def parse_detail(self, response, state, year):
        details = response.css('.row>a::attr(href)').get()
        with open('./data/state_acts.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Year', 'State', 'PDF Act']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'Year':year,
                'State':state,
                'PDF Act': response.urljoin(details)
            })