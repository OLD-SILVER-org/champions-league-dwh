from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from tasks.etl_old import ETLOldData  # Import the old ETL pipeline

# Initialize the ETL class
etl_old = ETLOldData()


# Function to execute the old ETL process
def run_etl_old():
    etl_old.run()


# Define the DAG
with DAG(
    dag_id="etl_old_dag",  # Unique identifier for the DAG
    schedule_interval="@daily",  # DAG runs daily
    start_date=datetime(2024, 3, 9),  # Start date for DAG execution
    catchup=False,  # Prevent execution of past DAG runs
) as dag:

    # Task to execute the old ETL process
    task_run_etl_old = PythonOperator(
        task_id="run_etl_old",  # Task name in Airflow
        python_callable=run_etl_old,  # Function to execute
    )

    # Define task execution order (single task in this case)
    task_run_etl_old
