import requests
import csv
import pandas as pd
import os
import sqlalchemy
from sqlalchemy import create_engine
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

    response_json = response.json()
    # print(response_json)
    return response_json


def create_dataframe():
    column_names = ['Phone Number', 'Validity', 'Spam', 'Country', 'Location',
                    'International Format', 'Type', 'Carrier']
    dataframe = pd.DataFrame(columns=column_names)
    return dataframe


def put_values_dataframe(dataframe, values):
    bool_column_names = ['Validity', 'Spam']
    dataframe[bool_column_names] = dataframe[bool_column_names].astype(bool)
    dataframe.loc[len(dataframe.index)] = values
    return dataframe


def is_spam(phone_number, spam_no_df):
    formatted_number = phone_number[1:len(phone_number)]
    result = spam_no_df[spam_no_df['Company_Phone_Number'] == formatted_number]
    return (len(result.index) != 0)


def get_values(data, spam_numbers):
    phone_number = data['phone']
    validity = data['valid']
    spam = is_spam(phone_number, spam_numbers)
    country = data['country']['name']
    location = data['location']
    international_format = data['format']['international']
    number_type = data['type']
    carrier = data['carrier']
    return phone_number, validity, spam, country, location,
           international_format, number_type, carrier


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


# def update_database(dbName, tableName, fileName):
#     load_database(dbName, fileName)
#     df = pd.read_sql_table(tableName, con=create_engine_function(dbName))

#     return loadNewData(df)


def check_database_input(phone_number, dataframe):
    phone_format = str(phone_number)
    result = dataframe[dataframe['Phone Number'] == phone_format]
    return (len(result.index) != 0), result


def check_validity(dataframe):
    if dataframe['Validity'].item() == 1:
        print(dataframe)

    else:
        print('The phone number you provided is invalid')


def main():
    # defining some terms
    tableName = 'validity_table'
    fileName = 'phone_number_file'
    dbName = 'phone_number_db'

    # spam numbers dataset/dataframe
    spam_numbers = pd.read_csv("dnc_complaint_numbers_2021-07-08.csv")

    # API keys
    abstract_api_key = '2240019ef22443bf83b96d9fc4599e31'
    numverify_key = 'c9c53eb9e5381913088a3aaa5b6555f8'

    phone_number = get_user_input()
    load_database(dbName, fileName)
    dtfr_initial = pd.read_sql_table(tableName,
                                     con=create_engine_function(dbName))
    is_in_db = check_database_input(phone_number, dtfr_initial)
    if is_in_db[0]:
        check_validity(is_in_db[1])
    else:
        data = get_data_from_api(phone_number, abstract_api_key)
        values = get_values(data, spam_numbers)

        # creating a new dataframe/database/SQL file
        # dataframe = create_dataframe()
        # dataframe_with_values = put_values_dataframe(dataframe, values)

        if values[1]:
            # using an existing database/SQL file
            dtfr_final = put_values_dataframe(dtfr_initial, values)
            save_data_to_file(dtfr_final, dbName, tableName, fileName)
            print(dtfr_final.tail(1))
        else:
            print('The phone number you provided is invalid')


if __name__ == "__main__":
    main()
