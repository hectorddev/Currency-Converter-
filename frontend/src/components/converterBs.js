import formatNumber from "./formatNumber"

const converter = (currency, value1, value2, mean_currencies) => {
    if(value1 === 'bs' && value2 === 'usd' 
        || value1 === 'bs' && value2 === 'cop' 
        || value1 === 'bs' && value2 === 'btc' 
        || value1 === 'bs' && value2 === 'bs'){
        const valueDolar = currency / mean_currencies.mean_usd_ves
        switch (value2) {
            case 'usd':
                return formatNumber(valueDolar, 'en-US', 'USD')
            case 'cop': 
                const bs_cop = valueDolar * mean_currencies.mean_usd_cop
                return formatNumber(bs_cop, 'es-CO', 'COP')
            case 'btc':
                return valueDolar / mean_currencies.mean_usd_btc
            default:
                break;
        }
    }  
}

export default converter