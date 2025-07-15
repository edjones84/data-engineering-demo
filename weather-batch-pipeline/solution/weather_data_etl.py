import sqlite3
import requests
import pandas as pd



def extract_data_as_json(url: str):
    '''
    Extracts JSON data from a given URL.
    This function sends a GET request to the specified URL and returns the JSON response.
    Raises an HTTPError for bad responses (4xx or 5xx).
    '''
    response = requests.get(url)
    response.raise_for_status()
    return response.json()



def transform_json_to_dataframe(data):
    ''' 
    Converts JSON data to a pandas DataFrame and processes it to extract relevant information.
    The function handles the structure of the JSON data, extracting current weather conditions and their units,           
    '''

    # Check if data is provided
    if not data:
        raise ValueError("No data provided to transform.")  
    

    # If data is a not list, convert it to a list
    if not isinstance(data, list):
        data = [data]
    
    
    all_dfs = []
    for entry in data:
        
        # Extract current weather data and units
        current = entry.get('current', {})
        current_units = entry.get('current_units', {})

        
        new_dict = {k: v for k, v in entry.items() if k not in ("current", "current_units")}

        
        # Build new column names with units
        for key in current:
            unit = current_units.get(key, '')
            col_name = f"{key}_{unit}" if unit else key
            new_dict[col_name] = current[key]
        
        

        df = pd.DataFrame(new_dict, index=[0])
        

        all_dfs.append(df)

    # Concatenate all DataFrames
    final_df = pd.concat(all_dfs, ignore_index=True)
    return final_df



def load_dataframe_to_sqllite_db(df: pd.DataFrame, db_path: str, table_name: str, time_col: str = "time_iso8601"):
    """
    Creates a table in SQLite database and appends new rows from the DataFrame if they do not already exist.
    If the table already exists, it checks for existing times and only appends new rows.
    """
    conn = sqlite3.connect(db_path)
    try:
        # Get existing times if table exists
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone():
            existing_times = pd.read_sql_query(f"SELECT {time_col} FROM {table_name}", conn)[time_col].tolist()
            df_to_append = df[~df[time_col].isin(existing_times)]
        else:
            df_to_append = df

        if not df_to_append.empty:
            df_to_append.to_sql(table_name, conn, if_exists='append', index=False)
            print(f"Appended {len(df_to_append)} new row(s) to '{table_name}' in '{db_path}'.")
        else:
            print("No new rows to append.")
    finally:
        conn.close()




def export_to_csv(db_path: str, table_name: str, file_path: str):
    '''
    Read all Data from specified table in SQLite database and export to CSV.
    '''
    conn = sqlite3.connect(db_path)
    countries_data = pd.read_sql_query(f"""select *
                                            from {table_name};""", conn)
    return countries_data.to_csv(file_path, index=False)



if __name__ == '__main__':
    try:
        json_data = extract_data_as_json(
            'https://api.open-meteo.com/v1/forecast?latitude=48.5,49,49.5,50,50.5,51&longitude=-2,-1,0,-2.5,-1.5,-0.5&current=wind_speed_10m,wind_direction_10m,temperature_2m,wind_gusts_10m,relative_humidity_2m,rain&forecast_days=1'
        )
        final_df = transform_json_to_dataframe(json_data)
        print(final_df.head())
        load_dataframe_to_sqllite_db(final_df, 'weather_data.db', 'weather', time_col='time_iso8601')
        export_to_csv('weather_data.db', 'weather', 'weatherData.csv')
    except Exception as e:
        print('Pipeline error: ' + str(e))
