from dagster import job, op, ScheduleDefinition, Definitions, DefaultScheduleStatus
import countries_db_extract
from datetime import datetime, timezone

START_TIME = datetime(2025, 6, 12, 6, 58, tzinfo=timezone.utc)

@op
def extract_op(context):
    url = 'http://api.worldbank.org/countries?format=json&per_page=100'
    countries_res = countries_db_extract.extract_countries_json_from_worldbank_api(url)
    context.log.info(f"Extracted {len(countries_res)} countries")
    return countries_res

@op
def load_op(context, countries_res):
    cur, conn = countries_db_extract.connect('pythonEtlDemo')
    countries_db_extract.load_data_to_sqllite_db(cur, conn, countries_res)
    context.log.info("Loaded data to SQLite DB")
    return 'pythonEtlDemo'

@op
def export_op(context, db_path):
    conn = countries_db_extract.connect(db_path)[1]
    countries_db_extract.export_to_csv(conn, 'countriesData.csv')
    context.log.info("Exported data to countriesData.csv")

@job
def countries_etl_job():
    countries = extract_op()
    db_path = load_op(countries)
    export_op(db_path)


# Schedule to run the job every 5 minutes
basic_schedule = ScheduleDefinition(
    job=countries_etl_job, 
    cron_schedule="*/5 * * * *",
    execution_timezone="UTC",
    default_status=DefaultScheduleStatus.RUNNING,
    description="Runs the countries ETL job every 5 minutes"
)

# Joins the job and schedule definitions into a single Definitions object
defs = Definitions(
    jobs=[countries_etl_job],
    schedules=[basic_schedule],
)