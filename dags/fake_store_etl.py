# dags/etl_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
#import sys
import pandas as pd
import logging

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar o diretório utils ao path para permitir importações dos scripts
#sys.path.append('/opt/airflow/dags')

# Importar as funções ETL
from utils.extract import extract_cart_data
from utils.transform import transform_cart_data
from utils.load import load_to_parquet

# Definir os argumentos padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['ivandouradorsd@gmail.com'],  # Substitua pelo seu email
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir a DAG
with DAG(
    'fake_store_etl',
    default_args=default_args,
    description='ETL para Fake Store API',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 10, 31),
    catchup=False,
) as dag:

    def extract():
        """
        Task de extração de dados.
        """
        try:
            df = extract_cart_data()
            # Salvar temporariamente os dados extraídos
            df.to_csv('/opt/airflow/dags/utils/data/carts.csv', index=False)
            logger.info("Task 'extract' concluída com sucesso.")
        except Exception as e:
            logger.error(f"Erro na task 'extract': {e}")
            raise

    def transform():
        """
        Task de transformação de dados.
        """
        try:
            # Carregar os dados extraídos
            df = pd.read_csv('/opt/airflow/dags/utils/data/carts.csv')
            transformed_df = transform_cart_data(df)
            # Salvar os dados transformados
            transformed_df.to_csv('/opt/airflow/dags/utils/data/transformed_carts.csv', index=False)
            logger.info("Task 'transform' concluída com sucesso.")
        except Exception as e:
            logger.error(f"Erro na task 'transform': {e}")
            raise

    def load():
        """
        Task de carregamento de dados.
        """
        try:
            # Carregar os dados transformados
            df = pd.read_csv('/opt/airflow/dags/utils/data/transformed_carts.csv')
            load_to_parquet(df)
            logger.info("Task 'load' concluída com sucesso.")
        except Exception as e:
            logger.error(f"Erro na task 'load': {e}")
            raise

    # Definir as tarefas
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load
    )

    # Definir a ordem das tarefas
    extract_task >> transform_task >> load_task
