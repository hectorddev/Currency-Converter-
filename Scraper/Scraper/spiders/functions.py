import json
import os
import csv
from datetime import datetime
import pandas as pd

#Verificacion de archivos

WDIR = os.getcwd()[:-24] if os.getcwd()[-7:] == 'spiders' else os.getcwd()
WDIR_IN = os.listdir(WDIR)

#Carpetas de archivos

EXPORT = os.path.join(WDIR,'export')
JSON_FILES = os.path.join(EXPORT,'json_files')
CSV_FILES = os.path.join(EXPORT,'history_files')

TRANSFORM = os.path.join(WDIR,'transform')
RAW_DATA = os.path.join(TRANSFORM,'raw_data')
CLEAN_DATA = os.path.join(TRANSFORM,'clean_data')

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
    if not 'export' in WDIR_IN and not 'transform' in WDIR_IN: #check if there are no such folders it creates it
        try:
            os.mkdir(EXPORT)
            os.mkdir(TRANSFORM)
        except FileExistsError:
            pass

    elif not 'export' in WDIR_IN: #check if not "export" folder 
        try:
            os.mkdir(EXPORT)
        except FileExistsError:
            pass    

    elif not 'transform' in WDIR_IN:
        try:
            os.mkdir(TRANSFORM) #check if not "transform" folder
        except FileExistsError:
            pass    


def _create_csv():
    """
    A function that creates a csv file
    """
    if not 'history_files' in os.listdir(EXPORT): #check if not "history" folder in EXPORT dir
        os.mkdir(CSV_FILES)
        with open(os.path.join(CSV_FILES, CSV_FILENAME), 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['mean_usd_cop','mean_usd_btc','mean_usd_ves','date'])

    elif 'history_files' in os.listdir(EXPORT): #check if "history" folder in EXPORT dir
        if not os.listdir(CSV_FILES):
            with open(os.path.join(CSV_FILES, CSV_FILENAME), 'w') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(['mean_usd_cop','mean_usd_btc','mean_usd_ves','date'])


def _create_json():
    """
    A function that create a json file
    """
    if not 'json_files' in os.listdir(EXPORT): #check if not "json_files" folder in EXPORT dir
        os.mkdir(JSON_FILES)
        dictionary ={}
        with open(os.path.join(JSON_FILES, JSON_FILENAME), "w") as outfile:
            json.dump(dictionary, outfile)

    else: #other conditionals
        if os.listdir(JSON_FILES): #check if something in "json_files" DIR 
            f = os.path.join(JSON_FILES,os.listdir(JSON_FILES)[0])
            os.remove(f)
            dictionary ={}
            with open(os.path.join(JSON_FILES, JSON_FILENAME), "w") as outfile:
                json.dump(dictionary, outfile)

        elif not os.listdir(JSON_FILES): #check if "json_files" is empty
            dictionary ={}
            with open(os.path.join(JSON_FILES, JSON_FILENAME), "w") as outfile:
                json.dump(dictionary, outfile) 

def verify():
    """
    A function that verfies if the csv and json files are in his folders
    if not it calls the function that create it 
    """
    _create_csv()
    _create_json()

    if not os.listdir(TRANSFORM): #check if "CLEAN DATA" and "RAW_DATA" folders exits in transform dir
        os.mkdir(CLEAN_DATA)
        os.mkdir(RAW_DATA)

    elif not 'clean_data' in os.listdir(TRANSFORM): #check "CLEAN_DATA" in transform dir
        os.mkdir(CLEAN_DATA)

    elif not 'raw_data' in os.listdir(TRANSFORM): #check "RAW_DATA" in transform dir
        os.mkdir(RAW_DATA)    

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
    data.append(DATE)
    #Adding data in a csv file   
    with open(os.path.join(CSV_FILES,CSV_FILENAME), 'a',newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)  

def _transform_ves(filename):
    """
    A function that transform raw data into a clean data using pandas
    it recieves a str (path) and returns an int
    """
    df = pd.read_csv(filename)
    transform = (df['value']
                .apply(lambda x: x.replace('VES',''))
                .apply(lambda x: x.replace(',','.'))
                .apply(lambda x: x.replace('\n',''))
                .apply(lambda x: x.replace('\r',''))
                .apply(lambda x: float(x))
                )

    df['value'] = transform

    df.to_csv(os.path.join(CLEAN_DATA,'clean_usd_ves.csv'))

    return round(df['value'].mean(),2)

def _transform_btc_cop(filename):
    """
    A function that transform raw data into clean data usinf pandas
    it recieves a str (path) and return an int
    """
    df = pd.read_csv(filename)
    transform = (df['value']
                .apply(lambda x: x.replace('\n',''))
                .apply(lambda x: x.replace('$',''))
                .apply(lambda x: x.replace(' ',''))
                .apply(lambda x: x[:6])
                .apply(lambda x: x.replace(',',''))
                .apply(lambda x: int(x.replace('.','')))
                )

    df['value'] = transform

    if 'usd_cop' in filename:
        df.to_csv(os.path.join(CLEAN_DATA,'clean_usd_cop.csv'))
    else:
        df.to_csv(os.path.join(CLEAN_DATA,'clean_usd_btc.csv'))
        
    return int(df['value'].mean())

def transform_data():
    """
    The main proccess that transform all the data collected and save 
    that data in csv history file and json file
    """
    mean_usd_cop = _transform_btc_cop(os.path.join(RAW_DATA,'raw_usd_cop.csv'))
    mean_usd_btc = _transform_btc_cop(os.path.join(RAW_DATA,'raw_usd_btc.csv'))
    mean_usd_ves = _transform_ves(os.path.join(RAW_DATA,'raw_usd_ves.csv'))
    _writeCsv([mean_usd_cop,mean_usd_btc,mean_usd_ves])
    _writeJson({'mean_usd_cop':mean_usd_cop,'mean_usd_btc':mean_usd_btc,'mean_usd_ves':mean_usd_ves})