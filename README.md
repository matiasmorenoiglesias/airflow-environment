# airflow-ingest-framework

Ejemplo de entorno con **Airflow 3.1**, Docker Compose y DAGs con **Datasets** para orquestación entre DAGs productor y consumidor.

---

## 📁 Estructura del proyecto

```text
.
├── dags/
│   ├── dag_productor.py
│   └── dag_consumidor.py
├── logs/
├── config/
│   ├── airflow.cfg
│   └── airflow_local_settings.py
├── docker-compose.yml
└── README.md
```

- **dags/**: contiene tus definiciones de DAGs  
- **logs/**: almacenamiento de logs de Airflow  
- **config/**: configuraciones personalizadas (cfg, local settings)  
- **docker-compose.yml**: define los servicios (api, scheduler, dag_processor, triggerer, postgres, etc.)

---

## 🛠 Requisitos

- Docker  
- Docker Compose (versión 3 o superior)  
- Conexión a internet para descargar imágenes

---

## 🚀 Levantando el entorno

```bash
make up
```

Luego verifica que el API responda:

```bash
curl http://0.0.0.0:8080/api/v2/monitor/health
```

Respuesta esperada (simplificada):

```json
{
  "metadatabase": {"status": "healthy"},
  "scheduler": {"status": "healthy"},
  "dag_processor": {"status": "healthy"}
}
```
Si necesitas bajar el entorno ejecuta este comando
```bash
make down
```

---

## 📂 DAGs de ejemplo

### DAG Productor — `dag_productor.py`

Este DAG genera un archivo CSV y lo publica como **Dataset**:

```python
from airflow import DAG, Dataset
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

ventas_dataset = Dataset("file:///tmp/datasets/ventas.csv")

def generar_datos():
    os.makedirs("/tmp/datasets", exist_ok=True)
    with open("/tmp/datasets/ventas.csv", "w") as f:
        f.write("fecha,ventas\n")
        f.write(f"{datetime.now().date()},1000\n")

with DAG(
    dag_id="dag_productor",
    start_date=datetime.now() - timedelta(days=1),
    schedule="@daily",
    catchup=False,
) as dag:
    generar_archivo = PythonOperator(
        task_id="generar_datos",
        python_callable=generar_datos,
        outlets=[ventas_dataset],
    )
```

### DAG Consumidor — `dag_consumidor.py`

Este DAG se ejecuta automáticamente cuando el dataset se actualiza:

```python
from airflow import DAG, Dataset
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import os

ventas_dataset = Dataset("file:///tmp/datasets/ventas.csv")

def procesar_datos():
    with open("/tmp/datasets/ventas.csv") as f:
        contenido = f.read()
    print(f"Contenido recibido:\n{contenido}")

with DAG(
    dag_id="dag_consumidor",
    start_date=datetime(2025, 1, 1),
    schedule=[ventas_dataset],
    catchup=False,
) as dag:
    procesar = PythonOperator(
        task_id="procesar_datos",
        python_callable=procesar_datos,
    )
```

---

## 🔄 Flujo de trabajo

1. El **DAG productor** escribe el archivo `/tmp/datasets/ventas.csv`.  
2. El `Dataset` detecta el cambio.  
3. Se dispara el **DAG consumidor** automáticamente.  
4. El consumidor lee el archivo y ejecuta su lógica.

---

## 🧰 Tips & Solución de problemas

- Asegúrate de usar URI válida: `file:///tmp/...` (tres slashes).  
- Si un DAG no aparece: revisa los logs del `dag_processor`.  
- Verifica que `AIRFLOW__CORE__EXECUTION_API_SERVER_URL` apunte a `http://api:8080/execution/` (no HTTPS).  
- Si usas docker, debes reemplaza la linea `D ?= podman` por `D ?= docker` en el archivo Makefile.


## ✅Buenas prácticas
- Escribe mensajes de commit claros y concisos.
- Usa ramas por feature o fix (para evitar trabajar directamente en main).
- Si es posible, actualiza la documentación (README.md, comentarios, etc.).
- Prueba tus cambios localmente antes de enviar un PR.
## 🐛 Reportar errores o sugerencias
Si encuentras un problema o quieres proponer una mejora, puedes abrir un Issue, detallando:
- Que estabas haciendo.
- Que esperabas que pasara.
- Que ocurrio.
- Logs, errores o capturas si es necesario.
## 📬 Contacto
Si prefieres, también puedes contactarme directamente por [LinkedIn](https://www.linkedin.com/in/matias-moreno-iglesias/) para charlar sobre ideas o propuestas relacionadas al proyecto.