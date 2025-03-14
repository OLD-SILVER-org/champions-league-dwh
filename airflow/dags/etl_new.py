from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/opt/airflow")

from tasks.etl_new import ETLNew  # Import the new ETL pipeline

# Initialize the ETL class
etl_new = ETLNew()


# Function to execute the new ETL process
def run_etl_new():
    etl_new.run()


# Define the DAG
with DAG(
    dag_id="etl_new_dag",  # Unique identifier for the DAG
    schedule_interval="@daily",  # DAG runs daily
    start_date=datetime(2024, 3, 9),  # Start date for DAG execution
    catchup=False,  # Prevent execution of past DAG runs
) as dag:

    # Task to execute the new ETL process
    task_run_etl_new = PythonOperator(
        task_id="run_etl_new",  # Task name in Airflow
        python_callable=run_etl_new,  # Function to execute
    )

    # Define task execution order (single task in this case)
    task_run_etl_new
