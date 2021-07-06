import requests
import pandas as pd
import os
import sqlalchemy
from sqlalchemy import create_engine_function
import matplotlib
import matplotlib.pyplot as plt


# test if the input is not empty and is a number
def get_user_input():
    user_input = input("Enter a phone number: ")
    return user_input
    

def get_data_from_api(phone_number, api_key):
    # abstract API
    abstract_api_base_url = "https://phonevalidation.abstractapi.com/v1/"
    response = requests.get(abstract_api_base_url + "?api_key=" + api_key +
                            "&phone=" + str(phone_number))
    
    # numverify API
    # numverify_base_url = 'http://apilayer.net/api/validate'
    # response = requests.get(numverify_base_url + "?access_key=" + api_key +
    #                        '&number=' + str(phone_number) + '&format=1')
    
    print(response.status_code)
    response_json = response.json()
    print(response_json)
    return response_json
    

def create_dataframe(values):
    column_names = ['Phone Number', 'Validity', 'Country', 'Location', 'Type',
                    'Carrier']
    dataframe = pd.DataFrame(columns=column_names)
    dataframe.loc[len(dataframe.index)] = values
    return dataframe
    

def get_values(data):
    phone_number = data['format']['international']
    validity = data['valid']
    country = data['country']['name']
    location = data['location']
    number_type = data['type']
    carrier = data['carrier']
    return phone_number, validity, country, location, number_type, carrier
    
    
def create_engine_function(dbName):
    return create_engine('mysql://root:codio@localhost/'
                         + dbName + '?charset=utf8', encoding='utf-8')


def write_table(dtfr, dbName, tableName):
    os.system('mysql -u root -pcodio -e\
              "CREATE DATABASE IF NOT EXISTS ' + dbName + ';"')
    dtfr.to_sql(tableName, con=create_engine_function(dbName),
                if_exists='replace', index=False)


def save_data_to_file(dtfr, dbName, tableName, fileName):
    dtfr.to_sql(tableName, con=create_engine_function(dbName),
                if_exists='replace',
                index=False)
    os.system('mysqldump -u root -pcodio {} > {}.sql'.format(dbName, fileName))


def load_database(dbName, fileName):
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '
              + dbName + '; "')
    os.system('mysql -u root -pcodio ' + dbName + ' < ' + fileName + '.sql')


def main():
    # Abstract API key
    abstract_api_key = '2240019ef22443bf83b96d9fc4599e31'
    numverify_key = 'c9c53eb9e5381913088a3aaa5b6555f8'
    phone_number = get_user_input()
    data = get_data_from_api(phone_number, abstract_api_key)
    values = get_values(data)
    dataframe = create_dataframe(values)
    print(dataframe)
    
    
if __name__ == "__main__":
    main()
