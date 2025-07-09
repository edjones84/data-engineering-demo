import sqlite3
import requests
import pandas as pd





def download_and_save_json_as_csv(url: str, filename: str):
    '''
    Downloads JSON data from the given URL, converts it to a pandas DataFrame,
    displays a sample, and saves the whole data as a CSV file.
    '''
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # If data is a list, get the first element
    if isinstance(data, list):
        data = data[0]
    
    # Extract hourly and hourly_units
    hourly = data.get('hourly', {})
    hourly_units = data.get('hourly_units', {})

    # Build new column names with units
    columns = []
    for key in hourly: 
        unit = hourly_units.get(key, '')
        col_name = f"{key}_{unit}" if unit else key
        columns.append(col_name)

    # Transpose the hourly data to rows
    rows = list(zip(*[hourly[key] for key in hourly]))
    df = pd.DataFrame(rows, columns=columns)

    # Add metadata columns (same value for all rows)
    metadata_keys = [
        "latitude", "longitude", "elevation", "generationtime_ms",
        "utc_offset_seconds", "timezone", "timezone_abbreviation"
    ]
    for key in metadata_keys:
        df[key] = data.get(key)

    print(df.head())
    df.to_csv(filename, index=False)

download_and_save_json_as_csv(
    'https://archive-api.open-meteo.com/v1/archive?latitude=51.51,48.85,52.52,40.42,41.9,52.37,48.21,59.33,52.23,37.98&longitude=-0.13,2.35,13.41,-3.7,12.5,4.9,16.37,18.07,21.01,23.73&start_date=2025-06-22&end_date=2025-07-07&hourly=temperature_2m,wind_speed_10m,rain,snowfall,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation,wind_direction_10m,wind_gusts_10m,cloud_cover_low,cloud_cover_mid,cloud_cover_high',
    'weather.csv'
)



# def connect(database_name: str):
#     ''' 
#     Connects to SQLlite and creates specified database object
#     '''
#     conn = sqlite3.connect(database_name)
#     cur = conn.cursor()
#     return cur, conn



# def load_data_to_sqllite_db(cursor, connect, countries_json):
#     '''
#     Creates countries table with three columns (id, name, capital_city) in SQLlite database using existing cursor and connect objects
    
#     Inserts data into countries table from countries json response of worldbank API
#     '''

#     try:
#         # Create table
#         cursor.executescript('''
#         DROP TABLE IF EXISTS countries;

#         CREATE TABLE countries (id varchar(5), name varchar(60), capital_city varchar(60))
#         ''')

#         # insert into table
#         for country in countries_json:
#             cursor.execute('INSERT INTO countries values (?,?,?)',
#                             [country['id'], country['name'], country['capitalCity']])
#             connect.commit()

#     except Exception as e:
#         print('Data Load Error : ' + str(e))




# def export_to_csv(connect, path: str):
#     '''
#     Read all Data from countries table and export to CSV
#     '''

#     countries_data = pd.read_sql_query(''' select *
#                                             from countries;
#                                          ''', connect)
#     return countries_data.to_csv(path, index=False)



# if __name__ == '__main__':
#     try:
#         countries_res = extract_countries_json_from_worldbank_api('http://api.worldbank.org/countries?format=json&per_page=100')
#         # cur, conn = connect('pythonEtlDemo') 
#         # load_data_to_sqllite_db(cur,conn, countries_res)
#         # export_to_csv(conn, 'countriesData.csv')
#     except Exception as e:
#         print('Pipeline error: ' + str(e))
