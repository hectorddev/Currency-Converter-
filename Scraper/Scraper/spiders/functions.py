import json
import os
import csv
from datetime import datetime

json_files = r'../../../Json_files/'
csv_files = r'../../../history_files/'
csv_files_in = os.listdir(csv_files)
json_files_in = os.listdir(json_files)
date =  datetime.now().strftime("%Y-%m-%d//%I:%M:%S%p")

def create_csv():
    """
    A function that creates a csv file
    """
    with open(csv_files + "mean_history.csv", 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['mean_usd_cop','mean_usd_btc','mean_usd_ves','date'])

def create_json():
    """
    A function that create a json file
    """  
    dictionary ={} 

    with open(json_files + "mean_currencies.json", "w") as outfile:
        json.dump(dictionary, outfile)

def verify():
    """
    A function that verfies if the csv and json files are in his folders
    if not it calls the function that create it 
    """
    if not csv_files_in:
        create_csv()
    if json_files_in:
        f = os.path.join(json_files,json_files_in[0])
        os.remove(f)
        create_json()
    else:
        create_json()  

def meanDict(data):
    """
    A function that calculate the mean of a dictionary
    """
    mean = sum([i for i in data.values()])/len(data)
    return round(mean,3)

def writeJson(path,name,dicti):
    """
    A function that write scraped data in a json file
    """
    with open(path + name, 'r+') as f:
            data = json.load(f)
            data.update(dicti)
            f.seek(0)
            json.dump(data,f)

def writeCsv(json_path,json_filename,csv_path,csv_filename):
    """
    A function that recieves 4 parameters that indicates the path and the name of the JSON file
    that we wanna read and the path and the name of the CSV file that we wanna write
    """
    #Reading json file
    with open(json_path + json_filename, 'r+') as f:
        data = json.load(f)
        content = sorted([i for i in data.values()])
        content.append(date)

    #Adding data in a csv file   
    with open(csv_path + csv_filename, 'a',newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(content)  

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
    
    


    