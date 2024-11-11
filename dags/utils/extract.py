# utils/extract.py

import requests
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_cart_data():
    """
    Extrai dados dos carrinhos de compras da Fake Store API.
    Retorna um DataFrame contendo os dados necessários.
    """
    FAKE_STORE_API_URL = os.getenv('FAKE_STORE_API_URL', 'https://fakestoreapi.com')
    url = f"{FAKE_STORE_API_URL}/carts"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        carts = response.json()

        # Converter a lista de carrinhos em um DataFrame
        df = pd.DataFrame(carts)
        logger.info("Dados extraídos com sucesso.")
        return df
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao extrair dados: {e}")
        return pd.DataFrame()
