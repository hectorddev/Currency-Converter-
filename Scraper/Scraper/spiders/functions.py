def meanDict(data):
    mean = sum([i for i in data.values()])/len(data)
    return round(mean,3)

def strSimple(currency):
    """
    a function that recieves a dirty str and cleans it, then returns a float
    currency is str
    """
    if 'E' in currency:
        currency = currency.replace('VES','')
        gumball = currency.replace('.','')
        gumball_s = gumball.replace(',','.')
        return float(gumball_s)

    if '\r' in currency:
        currency = currency.replace('\n','')
        currency = currency.replace('\r','')
        gumball = currency.replace('.','')
        gumball_s = gumball.replace(',','.')
        return float(gumball_s)

    if '$' in currency or '\n' in currency:
        another = currency.replace('$','')
        another_s = another.replace(',','')
        return float(another_s)

    if ' ' in currency:
        glassy = currency.replace(' ','')
        return float(glassy)

    if currency[1] == '.' or currency[2] == '.' or currency.count('.') >= 2:
        gumball = currency.replace('.','')
        gumball_s = gumball.replace(',','.')
        return float(gumball_s)

    else:
        wave = currency.replace(',','')
        return float(wave)
    
    


    