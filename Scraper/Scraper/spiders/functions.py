import json
import os
import csv
from datetime import datetime
import pandas as pd

#Verificacion de archivos

WDIR = os.getcwd()[:-24] if os.getcwd()[-7:] == 'spiders' else os.getcwd()
WDIR_IN = os.listdir(WDIR)

#Carpetas de archivos

JSON_FILES = os.path.join(WDIR,'json_files')
CSV_FILES = os.path.join(WDIR,'history_files')
RAW_DATA = os.path.join(WDIR,'raw_data')

#Fecha

DATE =  datetime.now().strftime("%Y-%m-%d//%I:%M:%S%p")

#Nombres de archivos

JSON_FILENAME = 'mean_currencies.json'
CSV_FILENAME = 'mean_history.csv'

def verify_folder():
    """
    a function that verifies if exits the folders that we need in the project
    if not, it creates those folders
    """
    if not 'history_files' in WDIR_IN and not 'json_files' in WDIR_IN and not 'raw_data' in WDIR_IN:
        try:
            os.mkdir(JSON_FILES)
            os.mkdir(CSV_FILES)
            os.mkdir(RAW_DATA)
        
        except FileExistsError as e:
            pass    

def create_csv():
    """
    A function that creates a csv file
    """
    with open(os.path.join(CSV_FILES, CSV_FILENAME), 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['mean_usd_cop','mean_usd_btc','mean_usd_ves','date'])

def create_json():
    """
    A function that create a json file
    """  
    dictionary ={}

    with open(os.path.join(JSON_FILES, JSON_FILENAME), "w") as outfile:
        json.dump(dictionary, outfile)

def verify():
    """
    A function that verfies if the csv and json files are in his folders
    if not it calls the function that create it 
    """
    if not os.listdir(CSV_FILES):
        create_csv()
    if os.listdir(JSON_FILES):
        f = os.path.join(JSON_FILES,os.listdir(JSON_FILES)[0])
        os.remove(f)
        create_json()
    else:
        create_json()  

def _writeJson(data):
    """
    A function that save transformed data in a json file
    it recieves a dictionary
    """
    with open(os.path.join(JSON_FILES,JSON_FILENAME), 'r+') as f:
            content = json.load(f)
            content.update(data)
            f.seek(0)
            json.dump(data,f)

def _writeCsv(data):
    """
    A function that recieves the save transformed data in a csv file
    it recieves a list
    """
    content = sorted(data)
    content.append(DATE)
    #Adding data in a csv file   
    with open(os.path.join(CSV_FILES,CSV_FILENAME), 'a',newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(content)  

def _transform_ves(filename):
    """
    A function that transform raw data into a clean data using pandas
    it recieves a list and returns an int
    """
    df = pd.read_csv(filename)
    transform = (df['value']
                .apply(lambda x: x.replace('VES',''))
                .apply(lambda x: x.replace('\r',''))
                .apply(lambda x: x.replace('\n',''))
                .apply(lambda x: x.replace(' ',''))
                .apply(lambda x: x.replace('.',''))
                .apply(lambda x: int(x[:7]) if x.count(',') >= 1 else int(x)) 
                )
    df['value'] = transform 
    return int(df['value'].mean())           

def _transform_btc_cop(filename):
    """
    A function that transform raw data into clean data usinf pandas
    it recieves a list and return an int
    """
    df = pd.read_csv(filename)
    transform = (df['value']
                .apply(lambda x: x.replace(',','.'))
                .apply(lambda x: x.replace('$',''))
                .apply(lambda x: x.replace('\n',''))
                .apply(lambda x: x.replace(' ',''))
                .apply(lambda x: x[:x.find('.')] + x[x.find('.') + 1:])
                .apply(lambda x: int(x[:x.find('.')]) if '.' in x else int(x))
                )
    df['value'] = transform 
    return int(df['value'].mean())

def transform_data():
    """
    The main proccess that transform all the data collected and save 
    that data in csv history file and json file
    """
    mean_usd_cop = _transform_btc_cop(os.path.join(RAW_DATA,'raw_usd_cop.csv'))
    mean_usd_btc = _transform_btc_cop(os.path.join(RAW_DATA,'raw_usd_btc.csv'))
    mean_usd_ves = _transform_ves(os.path.join(RAW_DATA,'raw_usd_ves.csv'))
    _writeCsv([mean_usd_btc,mean_usd_cop,mean_usd_ves])
    _writeJson({'mean_usd_cop':mean_usd_cop,'mean_usd_btc':mean_usd_btc,'mean_usd_ves':mean_usd_ves})