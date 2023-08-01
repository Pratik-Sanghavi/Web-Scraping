# my_crawl_script.py

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from india_code.spiders.central_acts import CentralActsSpider as SpiderCA

def run_spiders():
    process = CrawlerProcess(get_project_settings())

    process.crawl(SpiderCA)

    process.start()

if __name__ == "__main__":
    run_spiders()