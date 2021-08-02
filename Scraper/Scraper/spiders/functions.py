import json
import os
import csv

json_files = r'../../../Json_files/'
csv_files = r'../../../history_files/'
csv_files_in = os.listdir(csv_files)
json_files_in = os.listdir(json_files)

def create_csv():
    with open(csv_files + "mean_history.csv", 'w') as outfile:
        writer = csv.writer(outfile)

def create_json():  
    dictionary ={} 

    with open(json_files + "mean_currencies.json", "w") as outfile:
        json.dump(dictionary, outfile)

def verify():
    if not csv_files_in:
        create_csv()
    if json_files_in:
        f = os.path.join(json_files,json_files_in[0])
        os.remove(f)
        create_json()
    else:
        create_json()  

def meanDict(data):
    mean = sum([i for i in data.values()])/len(data)
    return round(mean,3)

def writeJson(path,name,dicti):
    with open(path + name, 'r+') as f:
            data = json.load(f)
            data.update(dicti)
            f.seek(0)
            json.dump(data,f)

def writeCsv():
    with open(json_files + "mean_currencies.json", 'r+') as f:
        data = json.load(f)
        rows = [i for i in data.keys()]
        content = [i for i in data.values()]
    with open(csv_files + "mean_history.csv", 'a',newline='') as outfile:
        writer = csv.DictWriter(outfile,fieldnames=rows)
        writer.writerow({rows[0]:content[0],rows[1]:content[1],rows[2]:content[2]})  

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
    
    


    