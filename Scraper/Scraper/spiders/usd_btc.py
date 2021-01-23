import scrapy
from functions import meanDict, strSimple

#Paginas de dolar-bitcoin

USD_BTC = ['https://coinmarketcap.com/es/currencies/bitcoin/', 'https://es.tradingview.com/symbols/BTCUSD/',
'https://www.marketwatch.com/investing/cryptocurrency/btcusd', 'https://www.coindesk.com/price/bitcoin']

# 1 investing = https://es.investing.com/crypto/bitcoin
# 2 coin_market_cap = https://coinmarketcap.com/es/currencies/bitcoin/
# 3 trading_view = https://es.tradingview.com/symbols/BTCUSD/
# 4 market_watch = https://www.marketwatch.com/investing/cryptocurrency/btcusd
# 5 coin_desk = https://www.coindesk.com/price/bitcoin

class usd_btc(scrapy.Spider):
    name = 'usd_btc'
    start_urls = [
        'https://es.investing.com/crypto/bitcoin'
    ]
    custom_settings = {
        'FEED_URI': 'currencies.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        investing_currency_btc = response.xpath('//div[@class="inlineblock"]/div[contains(@class,"top bold")]/span/span/text()').get()    
        test = strSimple(investing_currency_btc)
        yield {
            'test': test
        }