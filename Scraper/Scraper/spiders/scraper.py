import scrapy
import os
import pandas as pd
from scrapy.exceptions import CloseSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from functions import verify, verify_folder, transform_data

#Paginas de dolar-pesos

# investing = https://es.investing.com/currencies/usd-cop

USD_COL = ['https://www.mataf.net/es/cambio/divisas-USD-COP','https://www.dolar-colombia.com/',
'https://www.cotizacion.co/colombia/precio-del-dolar.php','https://dolar.wilkinsonpc.com.co/'] 

#Paginas de dolar-bitcoin

# 1 investing = https://es.investing.com/crypto/bitcoin

USD_BTC = ['https://coinmarketcap.com/es/currencies/bitcoin/', 'https://goldprice.org/es/cryptocurrency-price/bitcoin-price',
'https://www.marketwatch.com/investing/cryptocurrency/btcusd', 'https://www.coingecko.com/es/monedas/bitcoin']

#Paginas de dolar-bolivares

# 1 investing = https://es.investing.com/currencies/usd-vef

USD_VES = ['https://es.valutafx.com/USD-VES.htm', 'https://es.exchange-rates.org/Rate/USD/VES']

WDIR = os.getcwd()[:-24] if os.getcwd()[-7:] == 'spiders' else os.getcwd()
TRANSFORM = os.path.join(WDIR,'transform')
RAW_PATH = os.path.join(TRANSFORM,'raw_data')

class usd_cop(scrapy.Spider):
    name = 'usd_cop'
    start_urls = [
        'https://es.investing.com/currencies/usd-cop'
    ]
    
    def parse(self, response):
        investing_currency = response.xpath('//div[contains(@class,"overViewBox")]//div[contains(@class,"top")]/span[@id="last_last"]/text()').get()
        if investing_currency:
            yield response.follow(USD_COL[0], callback=self.mataf, cb_kwargs={'name':['investing'],'value':[investing_currency]})
        else:
            print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_cop \n'
                'method: parse \n'
                'page: investing colombia \n'
                )
        

    def mataf(self, response, **kwargs):
        mataf_currency = response.xpath('//div[@class="table-responsive"]/table/tbody[not(@class)]/tr[@itemprop="mainEntity"][1]/td[4]/span/meta[@itemprop="value"]/@content').get()
        if mataf_currency:
            mataf_currency = mataf_currency.replace(' ',',')
            kwargs['name'].append('mataf')
            kwargs['value'].append(mataf_currency)
            yield response.follow(USD_COL[1], callback=self.dolar_colombia ,cb_kwargs=kwargs)
        else:
           print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_cop \n'
                'method: mataf \n'
                'page: mataf \n'
                )   

    def dolar_colombia(self,response, **kwargs):
        dolar_colombia_currency = response.xpath('//div[@class="box"]/div[@class="box__content"]/h2/span/text()').get()
        if dolar_colombia_currency:
            kwargs['name'].append('dolar_colombia')
            kwargs['value'].append(dolar_colombia_currency)
            yield response.follow(USD_COL[2], callback=self.cotizacion, cb_kwargs=kwargs)
        else:
            print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_cop \n'
                'method: dolar_colombia \n'
                'page: dolar colombia \n'
                )    

    def cotizacion(self, response, **kwargs):
        cotizacion_currency = response.xpath('//div[contains(@class,"col-xs-12")]/p/span/span[@id="convertido-dol-ch"]/text()').get()
        if cotizacion_currency:
            kwargs['name'].append('cotizacion.co')
            kwargs['value'].append(cotizacion_currency)
            yield response.follow(USD_COL[3], callback=self.dolar_web, cb_kwargs=kwargs)
        else:
            print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_cop \n'
                'method: cotizacion \n'
                'page: cotzacion \n'
                )    

    def dolar_web(self,response,**kwargs):
        dolar_web = response.xpath('//div[@class="row"]//span[@class="valor"]/a/h2/span[@class="sube-numero"]/text()').get()
        dolar_web1 = response.xpath('//div[@class="row"]/div/span/a/h2/span[@class="baja-numero"]/text()').get()

        if dolar_web:
            kwargs['name'].append('dolar_web')
            kwargs['value'].append(dolar_web)

        else:
            kwargs['name'].append('dolar_web')
            kwargs['value'].append(dolar_web1)


        df = pd.DataFrame(kwargs,index=False)
        df.to_csv(os.path.join(RAW_PATH,'raw_usd_cop.csv'))

class usd_btc(scrapy.Spider):
    name = 'usd_btc'
    start_urls = [
        'https://es.investing.com/crypto/bitcoin'
    ]

    def parse(self, response):
        investing_currency_btc = response.xpath('//div[@class="inlineblock"]/div[contains(@class,"top bold")]/span/span/text()').get()    
        if investing_currency_btc:
            yield response.follow(USD_BTC[0], callback= self.coinmarketcap, cb_kwargs={'name':['investing'],'value':[investing_currency_btc]})
        else:
            print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_btc \n'
                'method: parse \n'
                'page: investing_currency \n'
                )    

    def coinmarketcap(self, response, **kwargs):
        coinmarket_currency_btc = response.xpath('//div[contains(@class,"sc")]/div[contains(@class,"priceValue")]/span/text()').get()    
        if coinmarket_currency_btc:
            kwargs['name'].append('coinmarketcap')
            kwargs['value'].append(coinmarket_currency_btc)
            yield response.follow(USD_BTC[1], callback = self.gold_price, cb_kwargs=kwargs)
        else:
            print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_btc \n'
                'method: coinmarketcap \n'
                'page: coinmarketcap \n'
                )      

    def gold_price(self, response, **kwargs):
        gold_price_currency_btc = response.xpath('//table[contains(@class,"views-table")]/tbody/tr[1]/td[contains(@class,"crypto-price")][1]/text()').get()
        if gold_price_currency_btc:
            kwargs['name'].append('gold_price')
            kwargs['value'].append(gold_price_currency_btc)
            yield response.follow(USD_BTC[2], callback = self.market_watch, cb_kwargs= kwargs)
        else:
            print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_btc \n'
                'method: gold_price \n'
                'page: gold price \n'
                )  

    def market_watch(self, response, **kwargs):
        market_watch_currency_btc = response.xpath('//div[@class="intraday__data"]/h2/bg-quote/text()').get()
        if market_watch_currency_btc:
            kwargs['name'].append('market_watch')
            kwargs['value'].append(market_watch_currency_btc)
            yield response.follow(USD_BTC[3], callback = self.coin_gecko, cb_kwargs= kwargs)
        else:
            print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_btc \n'
                'method: market_watch \n'
                'page: market watch \n'
                )  

    def coin_gecko(self, response, **kwargs):
        coin_gecko_currency_btc = response.xpath('//div[@data-controller="coins-information"]//span[@class="no-wrap" and @data-coin-id="1"]/text()').get()
        kwargs['name'].append('coin_gecko')
        kwargs['value'].append(coin_gecko_currency_btc)

        df = pd.DataFrame(kwargs,index=False)
        df.to_csv(os.path.join(RAW_PATH,'raw_usd_btc.csv'))

class usd_ves(scrapy.Spider):
    name = 'usd_ves'
    start_urls = [
        'https://es.investing.com/currencies/usd-vef'
    ]

    def parse(self, response):
        investing_currency_ves = response.xpath('//div[contains(@class,"overViewBox")]//div[contains(@class,"top")]/span[@id="last_last"]/text()').get()
        if investing_currency_ves:
            yield response.follow(USD_VES[0], callback = self.valutafx, cb_kwargs={'name':['investing'],'value':[investing_currency_ves]})
        else:
            print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_ves \n'
                'method: parse \n'
                'page: investing_currency_ves \n'
                )  

    def valutafx(self, response, **kwargs):
        valuta_currency_ves = response.xpath('//div[@class="converter-result"]/div[@class="rate-value"]/text()').get()
        if valuta_currency_ves:
            kwargs['name'].append('valuta')
            kwargs['value'].append(valuta_currency_ves)
            yield response.follow(USD_VES[1], callback = self.exchange_rates, cb_kwargs= kwargs)
        else:
            print('\n'
                'There is a problem with the xpath sentence \n'
                'Spider: usd_ves \n'
                'method: valutafx \n'
                'page: valutafx \n'
                )  

    def exchange_rates(self, response, **kwargs):
        exchange_rates_ves = response.xpath('//div[@class="table-responsive"]/table/tbody/tr[1]/td[contains(@class,"result")]/text()').get()
        kwargs['name'].append('exchange_rate')
        kwargs['value'].append(exchange_rates_ves)

        df = pd.DataFrame(kwargs,index=False)
        df.to_csv(os.path.join(RAW_PATH,'raw_usd_ves.csv'))

verify_folder()
verify()

configure_logging()
runner = CrawlerRunner(
    {
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    }
)

runner.crawl(usd_cop)
runner.crawl(usd_btc)
runner.crawl(usd_ves)

d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
transform_data()
