from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/opt/airflow")

from tasks.etl_old_data.player_old_etl import PlayerOldETL
from tasks.etl_old_data.squad_old_etl import SquadOldETL
from tasks.etl_old_data.score_old_etl import ScoreOldETL
from tasks.etl_old_data.match_old_etl import MatchOldETL

# Initialize ETL classes
player_etl = PlayerOldETL()
squad_etl = SquadOldETL()
score_etl = ScoreOldETL()
match_etl = MatchOldETL()


# Define functions for each ETL step
def process_player():
    player_etl.process()


def process_squad():
    squad_etl.process()


def process_score():
    score_etl.process()


def process_match():
    match_etl.process()


# Define DAG
with DAG(
    dag_id="etl_old_dag",
    schedule_interval=None,
    catchup=False,
) as dag:

    task_player = PythonOperator(
        task_id="process_old_player",
        python_callable=process_player,
    )

    task_squad = PythonOperator(
        task_id="process_old_squad",
        python_callable=process_squad,
    )

    task_score = PythonOperator(
        task_id="process_old_score",
        python_callable=process_score,
    )

    task_match = PythonOperator(
        task_id="process_old_match",
        python_callable=process_match,
    )

    # Define task execution order
    [task_player, task_squad, task_score] >> task_match
