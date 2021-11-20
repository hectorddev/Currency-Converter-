import formatNumber from "./formatNumber"

const converterBtc = (currency, value1, value2, mean_currencies) => {
    if(  value1 === 'btc' && value2 === 'usd' 
    || value1 === 'btc' && value2 === 'cop' 
    || value1 === 'btc' && value2 === 'btc' 
    || value1 === 'btc' && value2 === 'bs'){
        const btc = currency * mean_currencies.mean_usd_btc
        switch (value2) {
            case 'usd':
                return formatNumber(btc, 'en-US', 'USD') 
            case 'bs':
                const btc_bs = btc * mean_currencies.mean_usd_ves
                return formatNumber(btc_bs, 'es-VE', 'VED') 
            case 'cop':
                const btc_cop = btc * mean_currencies.mean_usd_cop
                return formatNumber(btc_cop, 'en-US', 'COP') 

            default:
                break;
        }
    }
}

export default converterBtc