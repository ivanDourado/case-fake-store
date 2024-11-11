# utils/load.py

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_to_parquet(df, output_path='/opt/airflow/dags/utils/output/user_cart_summary.parquet'):
    """
    Carrega os dados transformados em um arquivo Parquet.
    """
    try:
        # Garantir que o diretório de saída exista
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Salvar o DataFrame no formato Parquet
        df.to_parquet(output_path, index=False)
        logger.info(f"Dados salvos em {output_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
