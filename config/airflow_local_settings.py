import os
from airflow.config_templates.airflow_local_settings import DEFAULT_LOGGING_CONFIG

LOGGING_CONFIG = DEFAULT_LOGGING_CONFIG.copy()

base_log_folder = os.environ.get("AIRFLOW__LOGGING__BASE_LOG_FOLDER", "/opt/airflow/logs")

for handler_name, handler_conf in LOGGING_CONFIG["handlers"].items():
    if "filename" in handler_conf:
        # Reemplazar por una ruta absoluta en base a base_log_folder
        filename = os.path.basename(handler_conf["filename"])
        handler_conf["filename"] = os.path.join(base_log_folder, filename)
