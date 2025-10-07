from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG("soy_un_dag_de_ejemplo",
         start_date=datetime(2025, 1, 1),
         schedule=None,
         catchup=False) as dag:

    BashOperator(
        task_id="falla_con_echo",
        bash_command="echo 'Antes de fallar'; exit 0"
    )
