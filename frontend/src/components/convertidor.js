import converterBs from './converterBs'
import converterCop from './converterCop'
import converterUsd from './converterUsd'
import converterBtc from './converterBtc'

const convertidor = (valuesUser, mean_currencies) => {
    const {currency, value1, value2} = valuesUser

        
    if(value1 === value2){
        return new Intl.NumberFormat().format(currency)
    }

    switch (value1) {
        case 'bs':
            return converterBs(currency, value1, value2, mean_currencies)
        case 'cop':
            return converterCop(currency, value1, value2, mean_currencies)
        case 'usd':
            return converterUsd(currency, value1, value2, mean_currencies)
        case 'btc':
            return converterBtc(currency, value1, value2, mean_currencies)
        default:
            break;
    }
   
    
}

export default convertidor