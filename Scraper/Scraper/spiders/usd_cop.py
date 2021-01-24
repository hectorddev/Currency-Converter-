import scrapy
from functions import strSimple, meanDict

#Paginas de dolar-pesos

# investing = https://es.investing.com/currencies/usd-cop

USD_COL = ['https://www.mataf.net/es/cambio/divisas-USD-COP','https://www.dolar-colombia.com/',
'https://www.cotizacion.co/colombia/precio-del-dolar.php','https://dolar.wilkinsonpc.com.co/'] 

#Paginas de dolar-bolivares

# 1 investing = https://es.investing.com/currencies/usd-vef
# 2 the_money_converter = https://themoneyconverter.com/ES/USD/VES
# 3 valuta = https://es.valutafx.com/USD-VES.htm
# 4 cuex = https://cuex.com/es/usd-ves
# 5 exchange_rates = https://es.exchange-rates.org/Rate/USD/VES

class usd_cop(scrapy.Spider):
    name = 'usd_cop'
    start_urls = [
        'https://es.investing.com/currencies/usd-cop'
    ]
    custom_settings = {
        'FEED_URI': 'currencies_cop.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

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
        mean_usd_cop = meanDict(kwargs)
        yield {
            #'precio_usd_cop': kwargs,
            'media_usd_cop':mean_usd_cop
        }
    
 