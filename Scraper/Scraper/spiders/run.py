from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from functions import verify, writeCsv, verify_folder

JSON_PATH = r'../../../Json_files/'
JSON_FILENAME = 'mean_currencies.json'
CSV_PATH = r'../../../history_files/'
CSV_FILENAME = 'mean_history.csv'

def task():
    verify_folder()
    verify()
    proccess = CrawlerProcess(get_project_settings())
    proccess.crawl('usd_cop')
    proccess.crawl('usd_btc')
    proccess.crawl('usd_ves')
    proccess.start()    
    writeCsv(JSON_PATH,JSON_FILENAME,CSV_PATH,CSV_FILENAME)

task()