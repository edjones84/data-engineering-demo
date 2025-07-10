from dagster import job, op, ScheduleDefinition, Definitions, DefaultScheduleStatus
import weather_data_etl


@op
def extract_op(context):
    url = 'https://api.open-meteo.com/v1/forecast?latitude=48.5,49,49.5,50,50.5,51&longitude=-2,-1,0,-2.5,-1.5,-0.5&current=wind_speed_10m,wind_direction_10m,temperature_2m,wind_gusts_10m,relative_humidity_2m,rain&forecast_days=1'
    weather_res = weather_data_etl.extract_data_as_json(url)
    context.log.info(f"Extracted {len(weather_res)} rows of weather data")
    return weather_res

@op
def transform_op(context, weather_res):
    transformed_df = weather_data_etl.transform_json_to_dataframe(weather_res)
    context.log.info(f"Transformed data into DataFrame with {len(transformed_df)} rows")
    return transformed_df


@op()
def load_op(context, transformed_df):
    weather_data_etl.load_dataframe_to_sqllite_db(transformed_df, db_path='weather_data.db', table_name='weather', time_col='time_iso8601')
    context.log.info(f"Loading {len(transformed_df)} rows to SQLite DB")
    return 'weather_data.db'

@op
def export_op(context, db_path):
    weather_data_etl.export_to_csv(db_path, 'weather', 'weatherData.csv')
    context.log.info("Exported data to weatherData.csv")


@job
def weather_etl_job():
    weather_data = extract_op()
    transformed_data = transform_op(weather_data)
    db_path = load_op(transformed_data)
    export_op(db_path)


# Schedule to run the job every 5 minutes
basic_schedule = ScheduleDefinition(
    job=weather_etl_job, 
    cron_schedule="*/16 * * * *",
    execution_timezone="UTC",
    default_status=DefaultScheduleStatus.RUNNING,
    description="Runs the countries ETL job every 16 minutes"
)

# Joins the job and schedule definitions into a single Definitions object
defs = Definitions(
    jobs=[weather_etl_job],
    schedules=[basic_schedule],
)