from airflow import DAG, Dataset
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, date
import os

ventas_dataset = Dataset("file:///tmp/datasets/ventas.csv")

def generar_datos():
    print("Simulando generación de ventas.csv ...")
    os.makedirs("/tmp/datasets", exist_ok=True)
    with open("/tmp/datasets/ventas.csv", "w") as f:
        f.write("fecha,ventas\n")
        f.write(f"{date.today()},1000\n")
    print("Archivo ventas.csv generado correctamente ✅")

with DAG(
    dag_id="dag_productor",
    description="DAG productor que actualiza el dataset de ventas",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["semana1", "dataset", "productor"],
) as dag:

    generar_archivo = PythonOperator(
        task_id="generar_datos",
        python_callable=generar_datos,
        outlets=[ventas_dataset],
    )
