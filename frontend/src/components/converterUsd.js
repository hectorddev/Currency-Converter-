import formatNumber from "./formatNumber"

const converterUsd = (currency, value1, value2, mean_currencies) => {
    if(
        value1 === 'usd' && value2 === 'usd' 
        || value1 === 'usd' && value2 === 'cop' 
        || value1 === 'usd' && value2 === 'btc' 
        || value1 === 'usd' && value2 === 'bs'
    ){
        switch (value2) {
            case 'cop':
                const usd_cop = currency * mean_currencies.mean_usd_cop      
                return formatNumber(usd_cop, 'es-CO', 'COP')
            case 'btc':
                return currency / mean_currencies.mean_usd_btc
            case 'bs':
                const usd_bs = currency * mean_currencies.mean_usd_ves
                return formatNumber(usd_bs, 'es-VE', 'VED')
            default:
                break;
        }
    } 
}

export default converterUsd