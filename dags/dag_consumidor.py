from airflow import DAG, Dataset
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

ventas_dataset = Dataset("file:///tmp/datasets/ventas.csv")

def procesar_datos():
    print("Procesando datos de ventas actualizados...")
    with open("/tmp/datasets/ventas.csv") as f:
        contenido = f.read()
    print(f"Contenido recibido:\n{contenido}")
    print("Procesamiento completo ✅")

with DAG(
    dag_id="dag_consumidor",
    description="DAG consumidor que se ejecuta cuando se actualiza el dataset de ventas",
    start_date=datetime(2025, 1, 1),
    schedule=[ventas_dataset],  # se ejecuta cuando el dataset cambia
    catchup=False,
    tags=["semana1", "dataset", "consumidor"],
) as dag:

    procesar = PythonOperator(
        task_id="procesar_datos",
        python_callable=procesar_datos,
    )
