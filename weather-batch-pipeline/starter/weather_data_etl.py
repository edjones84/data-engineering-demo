import sqlite3
import requests
import pandas as pd


def extract_data_as_json(url: str):
    '''
    Extracts JSON data from a given URL.
    This function sends a GET request to the specified URL and returns the JSON response.
    Raises an HTTPError for bad responses (4xx or 5xx).
    '''
    pass




def transform_json_to_dataframe(data):
    ''' 
    Converts JSON data to a pandas DataFrame and processes it to extract relevant information.
    The function handles the structure of the JSON data, extracting current weather conditions and their units,           
    '''

    pass



def load_dataframe_to_sqllite_db():
    '''
    Creates a table in SQLite database and appends new rows from the DataFrame if they do not already exist.
    '''

    pass




def export_to_csv():
    '''
    Read all Data from specified table in SQLite database and export to CSV.
    '''
    pass



if __name__ == '__main__':
    try:
        ''' Main function to run the ETL process '''
        json_data = extract_data_as_json(
            'https://api.open-meteo.com/v1/forecast?latitude=48.5,49,49.5,50,50.5,51&longitude=-2,-1,0,-2.5,-1.5,-0.5&current=wind_speed_10m,wind_direction_10m,temperature_2m,wind_gusts_10m,relative_humidity_2m,rain&forecast_days=1'
        )
        print("Extracted JSON Data:", json_data)
    except Exception as e:
        ''' Handle any exceptions that occur during the ETL process '''
