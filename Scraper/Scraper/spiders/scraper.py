import scrapy
import json
from functions import strSimple, meanDict, verify
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

#Paginas de dolar-pesos

# investing = https://es.investing.com/currencies/usd-cop

USD_COL = ['https://www.mataf.net/es/cambio/divisas-USD-COP','https://www.dolar-colombia.com/',
'https://www.cotizacion.co/colombia/precio-del-dolar.php','https://dolar.wilkinsonpc.com.co/'] 

#Paginas de dolar-bitcoin

# 1 investing = https://es.investing.com/crypto/bitcoin

USD_BTC = ['https://coinmarketcap.com/es/currencies/bitcoin/', 'https://goldprice.org/es/cryptocurrency-price/bitcoin-price',
'https://www.marketwatch.com/investing/cryptocurrency/btcusd', 'https://www.coindesk.com/price/bitcoin']

#Paginas de dolar-bolivares

# 1 investing = https://es.investing.com/currencies/usd-vef

USD_VES = ['https://es.valutafx.com/USD-VES.htm', 'https://es.exchange-rates.org/Rate/USD/VES']

PATH = r'../../../Json_files/currencies.json'

verify()

class usd_cop(scrapy.Spider):
    name = 'usd_cop'
    start_urls = [
        'https://es.investing.com/currencies/usd-cop'
    ]
    
    def parse(self, response):
        investing_currency = response.xpath('//div[contains(@class,"overViewBox")]//div[contains(@class,"top")]/span[@id="last_last"]/text()').get()
        yield response.follow(USD_COL[0], callback=self.mataf, cb_kwargs={'investing':strSimple(investing_currency)})

    def mataf(self, response, **kwargs):
        mataf_currency = response.xpath('//div[@class="col-md-4"]//table[contains(@class,"table")]//span[not(@class)]/meta[@itemprop="value"]/@content').getall()[1]
        kwargs['mataf'] = strSimple(mataf_currency)
        yield response.follow(USD_COL[1], callback=self.dolar_colombia ,cb_kwargs=kwargs)

    def dolar_colombia(self,response, **kwargs):
        dolar_colombia_currency = response.xpath('//div[@class="box"]/div[@class="box__content"]/h2/span/text()').get()
        kwargs['dolar_colombia'] = strSimple(dolar_colombia_currency)
        yield response.follow(USD_COL[2], callback=self.cotizacion, cb_kwargs=kwargs)

    def cotizacion(self, response, **kwargs):
        cotizacion_currency = response.xpath('//div[contains(@class,"col-xs-12")]/p/span/span[@id="convertido-dol-ch"]/text()').get()
        kwargs['cotizacion.co'] = strSimple(cotizacion_currency)
        yield response.follow(USD_COL[3], callback=self.dolar_web, cb_kwargs=kwargs)

    def dolar_web(self,response,**kwargs):
        dolar_web = response.xpath('//div[@class="row"]//span[@class="valor"]/a/h2/span[@class="sube-numero"]/text()').get()
        kwargs['dolar_web'] = strSimple(dolar_web)
        mean_usd_cop = {'mean_usd_cop': meanDict(kwargs)}
        
        with open(PATH, 'r+') as f:
            data = json.load(f)
            data.update(mean_usd_cop)
            f.seek(0)
            json.dump(data,f)

class usd_btc(scrapy.Spider):
    name = 'usd_btc'
    start_urls = [
        'https://es.investing.com/crypto/bitcoin'
    ]

    def parse(self, response):
        investing_currency_btc = response.xpath('//div[@class="inlineblock"]/div[contains(@class,"top bold")]/span/span/text()').get()    
        yield response.follow(USD_BTC[0], callback= self.coinmarketcap, cb_kwargs={'investing': strSimple(investing_currency_btc)})

    def coinmarketcap(self, response, **kwargs):
        coinmarket_currency_btc = response.xpath('//div[contains(@class,"sc")]/div[contains(@class,"priceValue")]/text()').get()    
        kwargs['coinmarket'] = strSimple(coinmarket_currency_btc)
        yield response.follow(USD_BTC[1], callback = self.gold_price, cb_kwargs=kwargs)

    def gold_price(self, response, **kwargs):
        gold_price_currency_btc = response.xpath('//table[contains(@class,"views-table")]/tbody/tr[1]/td[contains(@class,"crypto-price")][1]/text()').get()
        kwargs['gold_price'] = strSimple(gold_price_currency_btc)
        yield response.follow(USD_BTC[2], callback = self.market_watch, cb_kwargs= kwargs)

    def market_watch(self, response, **kwargs):
        market_watch_currency_btc = response.xpath('//div[@class="intraday__data"]/h3/bg-quote/text()').get()
        kwargs['market_watch'] = strSimple(market_watch_currency_btc)
        yield response.follow(USD_BTC[3], callback = self.coin_desk, cb_kwargs= kwargs)

    def coin_desk(self, response, **kwargs):
        coin_desk_currency_btc = response.xpath('//div[@class="data-definition"]/div[@class="price-large"]/text()').get()
        kwargs['coin_desk'] = strSimple(coin_desk_currency_btc)
        mean_usd_btc = {'mean_usd_btc': meanDict(kwargs)}

        with open(PATH, 'r+') as f:
            data = json.load(f)
            data.update(mean_usd_btc)
            f.seek(0)
            json.dump(data,f)

class usd_ves(scrapy.Spider):
    name = 'usd_ves'
    start_urls = [
        'https://es.investing.com/currencies/usd-vef'
    ]

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
        mean_usd_ves = {'mean_usd_ves': meanDict(kwargs)}

        with open(PATH, 'r+') as f:
            data = json.load(f)
            data.update(mean_usd_ves)
            f.seek(0)
            json.dump(data,f)

proccess = CrawlerProcess(get_project_settings())
proccess.crawl(usd_cop)
proccess.crawl(usd_btc)
proccess.crawl(usd_ves)
proccess.start()