import logging
from airflow import DAG
from include.src.airflow.xcom import cleanup
from airflow.operators.dummy_operator import DummyOperator
from plugins.CoinGecko.operators.crypto_value_operator import CryptoValueOperator
log = logging.getLogger(__name__)
dag_id = "crypto_value_data_process"

# Default arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": '2025-01-01',
    'email_on_failure': False,
    "email_on_retry": False,
    'retries': 1
}

# Dag definition
with DAG(
        dag_id,
        default_args=default_args,
        schedule_interval='0 * * * *',
        catchup=False,
        on_failure_callback=cleanup,
        on_success_callback=cleanup,
        description='Retrive value of crypto currencies'
) as dag:
    dag.doc_md = __doc__

    start = DummyOperator(
        task_id='start',
        dag=dag
    )


    store_cyrpto_values = CryptoValueOperator(
        task_id='store_cyrpto_values',
        coins_id = ['bitcoin']
    )

    start >> store_cyrpto_values
