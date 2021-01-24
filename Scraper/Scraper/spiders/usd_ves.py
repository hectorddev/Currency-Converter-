import scrapy 
from functions import strSimple, meanDict

#Paginas de dolar-bolivares

# 1 investing = https://es.investing.com/currencies/usd-vef

USD_VES = ['https://es.valutafx.com/USD-VES.htm', 'https://es.exchange-rates.org/Rate/USD/VES']

# 5 exchange_rates = https://es.exchange-rates.org/Rate/USD/VES

class usd_ves(scrapy.Spider):
    name = 'usd_ves'
    start_urls = [
        'https://es.investing.com/currencies/usd-vef'
    ]
    custom_settings = {
        'FEED_URI': 'currencies_ves.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        investing_currency_ves = response.xpath('//div[contains(@class,"overViewBox")]//div[contains(@class,"top")]/span[@id="last_last"]/text()').get()
        yield response.follow(USD_VES[0], callback = self.valutafx, cb_kwargs={'investing': strSimple(investing_currency_ves)})

    def valutafx(self, response, **kwargs):
        valuta_currency_ves = response.xpath('//div[@class="converter-result"]/div[@class="rate-value"]/text()').get()
        kwargs['valuta'] = strSimple(valuta_currency_ves)
        yield response.follow(USD_VES[1], callback = self.exchange_rates, cb_kwargs= kwargs)

    def exchange_rates(self, response, **kwargs):
        exchange_rates_ves = response.xpath('//div[@class="table-responsive"]/table/tbody/tr[1]/td[contains(@class,"result")]/text()').get()
        kwargs['exchange_rate'] = strSimple(exchange_rates_ves)
        mean_usd_ves = meanDict(kwargs)
        yield{
            #'test': kwargs,
            'mean': mean_usd_ves
        }