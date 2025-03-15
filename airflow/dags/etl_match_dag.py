from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/opt/airflow")

from tasks.etl_match import ETL_match  # Import ETL class
from airflow.sensors.external_task import ExternalTaskSensor

# Sensor to wait for etl_new_score_dag completion
wait_for_score = ExternalTaskSensor(
    task_id="wait_for_score_dag",
    external_dag_id="etl_new_score_dag",
    external_task_id=None,
    mode="poke",
    poke_interval=60,
    timeout=7200,  # Timeout 2h
)
# Initialize the ETL class
etl_new = ETL_match()


# Define functions for each ETL step
def extract():
    etl_new.extract()


def transform():
    etl_new.transform()


def load():
    etl_new.load()


def load_to_dwh():
    etl_new.load_to_dwh()


# Define DAG
with DAG(
    dag_id="etl_new_match_dag",
    schedule_interval="@hourly",
    start_date=datetime(2024, 3, 9),
    catchup=False,
) as dag:

    task_extract = PythonOperator(
        task_id="extract_match",
        python_callable=extract,
    )

    task_transform = PythonOperator(
        task_id="transform_match",
        python_callable=transform,
    )

    task_load = PythonOperator(
        task_id="load_match",
        python_callable=load,
    )

    task_load_to_dwh = PythonOperator(
        task_id="load_to_dwh_match",
        python_callable=load_to_dwh,
    )

    # Define task execution order
wait_for_score >> task_extract >> task_transform >> task_load >> task_load_to_dwh
