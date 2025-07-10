from dagster import job, op, ScheduleDefinition, Definitions, DefaultScheduleStatus
import weather_data_etl


@op
def extract_op(context):
    pass
    

@op
def transform_op(context, weather_res):
    pass
    


@op()
def load_op(context, transformed_df):
    pass
    

@op
def export_op(context, db_path):
    pass
    


@job
def weather_etl_job():
    pass
    


# Schedule to run the job every 5 minutes


# Joins the job and schedule definitions into a single Definitions object
