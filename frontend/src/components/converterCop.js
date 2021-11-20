import formatNumber from "./formatNumber"

const converterCop = (currency, value1, value2, mean_currencies) => {
    if(
        value1 === 'cop' && value2 === 'usd'  
        || value1 === 'cop' && value2 === 'btc' 
        || value1 === 'cop' && value2 === 'bs'
    ){
        console.log(currency)
        const valuePeso_Dolar = currency / mean_currencies.mean_usd_cop
        console.log(valuePeso_Dolar)
        switch (value2) {
            case 'usd': 
                return formatNumber(valuePeso_Dolar, 'en-US', 'USD')
            case 'btc':
                return valuePeso_Dolar / mean_currencies.mean_usd_btc
            case 'bs': 
                const cop_bs = valuePeso_Dolar * mean_currencies.mean_usd_ves
                return formatNumber(cop_bs, 'es-VE', 'VED')
            default:
                break;
        }
    }
}

export default converterCop