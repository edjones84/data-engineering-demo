import sqlite3
import requests
import pandas as pd


def extract_countries_json_from_worldbank_api(url: str):
    '''
    Extracts Countries JSON data from worldbank API
    '''
    pass




def connect(database_name: str):
    ''' 
    Connects to SQLlite and creates specified database object
    '''
    pass



def load_data_to_sqllite_db(cursor, connect, countries_json):
    '''
    Creates countries table with three columns (id, name, capital_city) in SQLlite database using existing cursor and connect objects
    
    Inserts data into countries table from countries json response of worldbank API
    '''

    pass




def export_to_csv(connect, path: str):
    '''
    Read all Data from countries table and export to CSV
    '''
    pass



if __name__ == '__main__':
    try:
        ''' Main function to run the ETL process '''
    except Exception as e:
        ''' Handle any exceptions that occur during the ETL process '''
