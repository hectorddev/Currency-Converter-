import scrapy
from functions import meanDict, strSimple

#Paginas de dolar-bitcoin

# 1 investing = https://es.investing.com/crypto/bitcoin
USD_BTC = ['https://coinmarketcap.com/es/currencies/bitcoin/', 'https://goldprice.org/es/cryptocurrency-price/bitcoin-price',
'https://www.marketwatch.com/investing/cryptocurrency/btcusd', 'https://www.coindesk.com/price/bitcoin']

class usd_btc(scrapy.Spider):
    name = 'usd_btc'
    start_urls = [
        'https://es.investing.com/crypto/bitcoin'
    ]
    custom_settings = {
        'FEED_URI': 'currencies_btc.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

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
        mean_usd_btc = meanDict(kwargs)
        yield{
            #'prices_btc': kwargs,
            'mean_usd_btc': mean_usd_btc
        }  