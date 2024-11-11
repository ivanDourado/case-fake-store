# utils/transform.py

import pandas as pd
from datetime import datetime
import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = requests.Session()

def transform_cart_data(df_carts):
    """
    Transforma os dados extraídos.
    Retorna um DataFrame com:
      - identificador de usuário
      - data mais recente em que o usuário adicionou produtos ao carrinho
      - categoria com mais produtos adicionados ao carrinho
    """
    user_data = {}

    for _, row in df_carts.iterrows():
        user_id = row['userId']
        cart_date = datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        products = row['products']

        if user_id not in user_data:
            user_data[user_id] = {
                'latest_cart_date': cart_date,
                'categories': {}
            }
        else:
            if cart_date > user_data[user_id]['latest_cart_date']:
                user_data[user_id]['latest_cart_date'] = cart_date

        for product in products:
            product_id = product['productId']
            category = get_product_category(product_id)
            if category:
                if category in user_data[user_id]['categories']:
                    user_data[user_id]['categories'][category] += 1
                else:
                    user_data[user_id]['categories'][category] = 1

    # Preparar os dados finais
    final_data = []
    for user_id, data in user_data.items():
        # Determinar a categoria mais frequente
        if data['categories']:
            top_category = max(data['categories'], key=data['categories'].get)
        else:
            top_category = None
        final_data.append({
            'user_id': user_id,
            'latest_cart_date': data['latest_cart_date'],
            'top_category': top_category
        })

    final_df = pd.DataFrame(final_data)
    logger.info("Dados transformados com sucesso.")
    return final_df

def get_product_category(product_id):
    """
    Obtém a categoria de um produto específico.
    Utiliza uma sessão persistente para otimizar as requisições.
    """
    FAKE_STORE_API_URL = os.getenv('FAKE_STORE_API_URL', 'https://fakestoreapi.com')
    url = f"{FAKE_STORE_API_URL}/products/{product_id}"
    try:
        response = session.get(url)
        response.raise_for_status()
        product = response.json()
        category = product.get('category')
        logger.info(f"Produto {product_id} pertence à categoria '{category}'.")
        return category
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao obter categoria do produto {product_id}: {e}")
        return None
