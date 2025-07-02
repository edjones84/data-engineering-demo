import sqlite3
import requests
import pandas as pd


def extract_countries_json_from_worldbank_api(url: str):
    '''
    Extracts Countries JSON data from worldbank API
    '''
    response = requests.get(url)
    return response.json()[1]




def connect(database_name: str):
    ''' 
    Connects to SQLlite and creates specified database object
    '''
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    return cur, conn



def load_data_to_sqllite_db(cursor, connect, countries_json):
    '''
    Creates countries table with three columns (id, name, capital_city) in SQLlite database using existing cursor and connect objects
    
    Inserts data into countries table from countries json response of worldbank API
    '''

    try:
        # Create table
        cursor.executescript('''
        DROP TABLE IF EXISTS countries;

        CREATE TABLE countries (id varchar(5), name varchar(60), capital_city varchar(60))
        ''')

        # insert into table
        for country in countries_json:
            cursor.execute('INSERT INTO countries values (?,?,?)',
                            [country['id'], country['name'], country['capitalCity']])
            connect.commit()

    except Exception as e:
        print('Data Load Error : ' + str(e))




def export_to_csv(connect, path: str):
    '''
    Read all Data from countries table and export to CSV
    '''

    countries_data = pd.read_sql_query(''' select *
                                            from countries;
                                         ''', connect)
    return countries_data.to_csv(path, index=False)



if __name__ == '__main__':
    try:
        countries_res = extract_countries_json_from_worldbank_api('http://api.worldbank.org/countries?format=json&per_page=100')
        cur, conn = connect('pythonEtlDemo') 
        load_data_to_sqllite_db(cur,conn, countries_res)
        export_to_csv(conn, 'countriesData.csv')
    except Exception as e:
        print('Pipeline error: ' + str(e))
