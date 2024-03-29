import scrapy
import os
import pandas as pd
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from functions import verify, verify_folder, transform_data, error_message

#Paginas de dolar-pesos

# investing = https://es.investing.com/currencies/usd-cop

USD_COL = {'mataf': 'https://www.mataf.net/es/cambio/divisas-USD-COP', 'dolar_colombia':'https://www.dolar-colombia.com/',
'cotizacion':'https://www.cotizacion.co/colombia/precio-del-dolar.php','dolar_web':'https://dolar.wilkinsonpc.com.co/'} 

#Paginas de dolar-bitcoin

# 1 investing = https://es.investing.com/crypto/bitcoin

USD_BTC = {'coinmarketcap':'https://coinmarketcap.com/es/currencies/bitcoin/','coin_telegraph':'https://cointelegraph.com/bitcoin-price',
'marketwatch':'https://www.marketwatch.com/investing/cryptocurrency/btcusd', 'yahoo_finance':'https://finance.yahoo.com/quote/BTC-USD'}

#Paginas de dolar-bolivares

# 1 investing = https://es.investing.com/currencies/usd-vef

USD_VES = {'valutafx':'https://es.valutafx.com/USD-VES.htm', 'exchange':'https://es.exchange-rates.org/Rate/USD/VES'}

WDIR = os.getcwd()[:-24] if os.getcwd()[-7:] == 'spiders' else os.getcwd()
TRANSFORM = os.path.join(WDIR,'transform')
RAW_PATH = os.path.join(TRANSFORM,'raw_data')

class usd_cop(scrapy.Spider):
    name = 'usd_cop'
    start_urls = [
        'https://es.investing.com/currencies/usd-cop'
    ]
    
    def parse(self, response):
        investing_currency = response.xpath('//div[contains(@class,"instrument-price")]/span[@data-test="instrument-price-last" and @class="text-2xl"]/text()').get()
        if investing_currency:
            yield response.follow(USD_COL['mataf'], callback=self.mataf, cb_kwargs={'name':['investing'],'value':[investing_currency]})
        else:
            error_message('usd_cop','parse','https://es.investing.com/currencies/usd-cop')
            yield response.follow(USD_COL['mataf'], callback=self.mataf, cb_kwargs={'name':['investing'],'value':['not available']})        

    def mataf(self, response, **kwargs):
        mataf_currency = response.xpath('//div[@class="table-responsive"]/table/tbody[not(@class)]/tr[@itemprop="mainEntity"][1]/td[4]/span/meta[@itemprop="value"]/@content').get()
        if mataf_currency:
            mataf_currency = mataf_currency.replace(' ',',')
            kwargs['name'].append('mataf')
            kwargs['value'].append(mataf_currency)
            yield response.follow(USD_COL['dolar_colombia'], callback=self.dolar_colombia ,cb_kwargs=kwargs)
        else:
            error_message('usd_cop','mataf',USD_COL['mataf'])
            kwargs['name'].append('mataf')
            kwargs['value'].append('not available')
            yield response.follow(USD_COL['dolar_colombia'], callback=self.dolar_colombia ,cb_kwargs=kwargs)       

    def dolar_colombia(self,response, **kwargs):
        dolar_colombia_currency = response.xpath('//div[@class="box"]/div[@class="box__content"]/h2/span/text()').get()
        if dolar_colombia_currency:
            kwargs['name'].append('dolar_colombia')
            kwargs['value'].append(dolar_colombia_currency)
            yield response.follow(USD_COL['cotizacion'], callback=self.cotizacion, cb_kwargs=kwargs)
        else:
            error_message('usd_cop','dolar_colombia',USD_COL['dolar_colombia'])
            kwargs['name'].append('dolar_colombia')
            kwargs['value'].append('not available')
            yield response.follow(USD_COL['cotizacion'], callback=self.cotizacion, cb_kwargs=kwargs)        

    def cotizacion(self, response, **kwargs):
        cotizacion_currency = response.xpath('//div[contains(@class,"col-xs-12")]/p/span/span[@id="convertido-dol-ch"]/text()').get()
        if cotizacion_currency:
            kwargs['name'].append('cotizacion.co')
            kwargs['value'].append(cotizacion_currency)
            yield response.follow(USD_COL['dolar_web'], callback=self.dolar_web, cb_kwargs=kwargs)
        else:
            error_message('usd_cop','cotizacion',USD_COL['cotizacion'])
            kwargs['name'].append('cotizacion.co')
            kwargs['value'].append('not available')
            yield response.follow(USD_COL['dolar_web'], callback=self.dolar_web, cb_kwargs=kwargs)       

    def dolar_web(self,response,**kwargs):
        dolar_web = response.xpath('//div[@class="row"]//span[@class="valor"]/a/h2/span[@class="sube-numero"]/text()').get()
        dolar_web1 = response.xpath('//div[@class="row"]/div/span/a/h2/span[@class="baja-numero"]/text()').get()

        if dolar_web:
            kwargs['name'].append('dolar_web')
            kwargs['value'].append(dolar_web)

        else:
            kwargs['name'].append('dolar_web')
            kwargs['value'].append(dolar_web1)

        df = pd.DataFrame(kwargs)
        df.to_csv(os.path.join(RAW_PATH,'raw_usd_cop.csv'))

class usd_btc(scrapy.Spider):
    name = 'usd_btc'
    start_urls = [
        'https://es.investing.com/crypto/bitcoin'
    ]

    def parse(self, response):
        investing_currency_btc = response.xpath('//div[@class="inlineblock"]/div[contains(@class,"top bold")]/span/span/text()').get()    
        if investing_currency_btc:
            yield response.follow(USD_BTC['coinmarketcap'], callback= self.coinmarketcap, cb_kwargs={'name':['investing'],'value':[investing_currency_btc]})
        else:
            error_message('usd_btc','parse',USD_BTC['https://es.investing.com/crypto/bitcoin'])
        yield response.follow(USD_BTC['coinmarketcap'], callback= self.coinmarketcap, cb_kwargs={'name':['investing'],'value':['not available']})           

    def coinmarketcap(self, response, **kwargs):
        coinmarket_currency_btc = response.xpath('//div[contains(@class,"sc")]/div[contains(@class,"priceValue")]/span/text()').get()    
        if coinmarket_currency_btc:
            kwargs['name'].append('coinmarketcap')
            kwargs['value'].append(coinmarket_currency_btc)
            yield response.follow(USD_BTC['coin_telegraph'], callback = self.coin_telegraph, cb_kwargs=kwargs)
        else:
            error_message('usd_btc','coinmarketcap',USD_BTC['coinmarketcap'])
            kwargs['name'].append('coinmarketcap')
            kwargs['value'].append('not available')
            yield response.follow(USD_BTC['coin_telegraph'], callback = self.coin_telegraph, cb_kwargs=kwargs)          

    def coin_telegraph(self, response, **kwargs):
        coin_telegraph_currency_btc = response.xpath('//span[@class="price-value" and contains(text(),"$")]/text()').get()
        if coin_telegraph_currency_btc:
            kwargs['name'].append('coin_telegraph')
            kwargs['value'].append(coin_telegraph_currency_btc)
            yield response.follow(USD_BTC['marketwatch'], callback = self.market_watch, cb_kwargs= kwargs)
        else:
            error_message('usd_btc','coin_telegraph',USD_BTC['coin_telegraph'])
            kwargs['name'].append('coin_telegraph')
            kwargs['value'].append('not_available')
            yield response.follow(USD_BTC['marketwatch'], callback = self.market_watch, cb_kwargs= kwargs)

    def market_watch(self, response, **kwargs):
        market_watch_currency_btc = response.xpath('//div[@class="intraday__data"]/h2/bg-quote/text()').get()
        if market_watch_currency_btc:
            kwargs['name'].append('market_watch')
            kwargs['value'].append(market_watch_currency_btc)
            yield response.follow(USD_BTC['yahoo_finance'], callback = self.yahoo_finance, cb_kwargs= kwargs)
        else:
            error_message('usd_btc','marketwatch',USD_BTC['marketwatch'])
            kwargs['name'].append('market_watch')
            kwargs['value'].append('not available')
            yield response.follow(USD_BTC['yahoo_finance'], callback = self.yahoo_finance, cb_kwargs= kwargs)    

    def yahoo_finance(self, response, **kwargs):
        yahoo_finance_currency_btc = response.xpath('//fin-streamer[@data-symbol="BTC-USD" and @value and @data-test="qsp-price"]/@value').get()
        kwargs['name'].append('yahoo_finance')
        kwargs['value'].append(yahoo_finance_currency_btc)

        df = pd.DataFrame(kwargs)
        df.to_csv(os.path.join(RAW_PATH,'raw_usd_btc.csv'))

class usd_ves(scrapy.Spider):
    name = 'usd_ves'
    start_urls = [
        'https://es.investing.com/currencies/usd-vef'
    ]

    def parse(self, response):
        investing_currency_ves = response.xpath('//div[contains(@class,"instrument-price")]/span[@data-test="instrument-price-last" and @class="text-2xl"]/text()').get()
        if investing_currency_ves:
            yield response.follow(USD_VES['valutafx'], callback = self.valutafx, cb_kwargs={'name':['investing'],'value':[investing_currency_ves]})
        else:
            error_message('usd_ves','parse',USD_VES['https://es.investing.com/currencies/usd-vef'])
            yield response.follow(USD_VES['valutafx'], callback = self.valutafx, cb_kwargs={'name':['investing'],'value':['not available']})

    def valutafx(self, response, **kwargs):
        valuta_currency_ves = response.xpath('//div[@class="converter-result"]/div[@class="rate-value"]/text()').get()
        if valuta_currency_ves:
            kwargs['name'].append('valuta')
            kwargs['value'].append(valuta_currency_ves)
            yield response.follow(USD_VES['exchange'], callback = self.exchange_rates, cb_kwargs= kwargs)
        else:
            error_message('usd_ves','valutafx',USD_VES['valutafx'])
            kwargs['name'].append('valuta')
            kwargs['value'].append('not available')
            yield response.follow(USD_VES['exchange'], callback = self.exchange_rates, cb_kwargs= kwargs)      

    def exchange_rates(self, response, **kwargs):
        exchange_rates_ves = response.xpath('//div[@class="table-responsive"]/table/tbody/tr[1]/td[contains(@class,"result")]/text()').get()
        kwargs['name'].append('exchange_rate')
        kwargs['value'].append(exchange_rates_ves)

        df = pd.DataFrame(kwargs)
        df.to_csv(os.path.join(RAW_PATH,'raw_usd_ves.csv'))

if __name__ == '__main__':
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
