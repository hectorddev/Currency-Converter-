import scrapy
from functions import strSimple

#Paginas de dolar-pesos

USD_COL = ['https://www.mataf.net/es/cambio/divisas-USD-COP','https://www.dolar-colombia.com/',
'https://www.cotizacion.co/colombia/precio-del-dolar.php','https://dolar.wilkinsonpc.com.co/'] 
#1 dolar_colombia = 'https://www.dolar-colombia.com/'
#2 mataf = https://www.mataf.net/es/cambio/divisas-USD-COP
#3 investing = https://es.investing.com/currencies/usd-cop
#4 cotizacion = 'https://www.cotizacion.co/colombia/precio-del-dolar.php'
#5 dolar_Web = https://dolar.wilkinsonpc.com.co/

#Paginas de dolar-bitcoin

# 1 investing = https://es.investing.com/crypto/bitcoin
# 2 coin_market_cap = https://coinmarketcap.com/es/currencies/bitcoin/
# 3 trading_view = https://es.tradingview.com/symbols/BTCUSD/
# 4 market_watch = https://www.marketwatch.com/investing/cryptocurrency/btcusd
# 5 coin_desk = https://www.coindesk.com/price/bitcoin

#Paginas de dolar-bolivares

# 1 investing = https://es.investing.com/currencies/usd-vef
# 2 the_money_converter = https://themoneyconverter.com/ES/USD/VES
# 3 valuta = https://es.valutafx.com/USD-VES.htm
# 4 cuex = https://cuex.com/es/usd-ves
# 5 exchange_rates = https://es.exchange-rates.org/Rate/USD/VES

class scraper(scrapy.Spider):
    name = 'Scraper'
    start_urls = [
        'https://es.investing.com/currencies/usd-cop'
    ]
    custom_settings = {
        'FEED_URI': 'currencies.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        investing_currencie = response.xpath('//div[contains(@class,"overViewBox")]//div[contains(@class,"top")]/span[@id="last_last"]/text()').get()
        yield {
            'investing':strSimple(investing_currencie)
        }