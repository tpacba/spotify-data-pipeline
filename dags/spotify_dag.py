from datetime import timedelta
from airflow import DAG
from airflow.operators.python import task
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.timezone import datetime

default_args = {
    "owner": 'airflow',
    "depends_on_past": False,
    "start_date": datetime(2021,2,15),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    "spotify_dag",
    default_args=default_args,
    description="Spotify DAG with ETL process",
    schedule_interval=timedelta(days=1)
)

def success_print():
    print("Success!")

run_etl = PythonOperator(
    task_id="whole_spotify_etl",
    python_callable=success_print,
    dag=dag
)

run_etl