from scraper import usd_cop, usd_btc, usd_ves
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from functions import verify, verify_folder, transform_data

def task():
    verify_folder()
    verify()
    proccess = CrawlerProcess(get_project_settings())
    proccess.crawl(usd_cop)
    proccess.crawl(usd_btc)
    proccess.crawl(usd_ves)
    proccess.start()
    transform_data()

task()