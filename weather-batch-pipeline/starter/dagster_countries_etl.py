from dagster import job, op, ScheduleDefinition, Definitions, DefaultScheduleStatus
import countries_db_extract
from datetime import datetime, timezone

START_TIME = datetime(2025, 6, 12, 6, 58, tzinfo=timezone.utc)

@op
def extract_op(context):
    pass

@op
def load_op(context, countries_res):
    pass

@op
def export_op(context, db_path):
    pass

@job
def countries_etl_job():
    pass


#Schedule to run the job every 5 minutes

#