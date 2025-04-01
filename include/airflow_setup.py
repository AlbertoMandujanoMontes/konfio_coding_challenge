import json
from airflow.models import Connection, Variable
from airflow.utils.db import provide_session
from airflow import settings
import yaml

@provide_session
def load_settings_from_yaml(session=None):
    with open("/opt/airflow/airflow_settings.yaml") as f:
        config = yaml.safe_load(f)

    for conn in config.get("airflow", {}).get("connections", []):
        conn_obj = Connection(
            conn_id=conn["conn_id"],
            conn_type=conn["conn_type"],
            host=conn.get("conn_host"),
            schema=conn.get("conn_schema"),
            login=conn.get("conn_login"),
            password=conn.get("conn_password"),
            port=int(conn.get("conn_port")) if conn.get("conn_port") else None,
            extra=conn.get("conn_extra")
        )
        session.merge(conn_obj)

    for var in config.get("airflow", {}).get("variables", []):
        Variable.set(var["variable_name"], var["variable_value"])

    session.commit()

load_settings_from_yaml()
