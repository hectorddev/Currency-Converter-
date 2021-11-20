function formatNumber(number, dataLocals, currency){
    return new Intl.NumberFormat( {locales: dataLocals} , {
        style: 'currency', 
        currency: currency
    }).format(number)
}

export default formatNumber