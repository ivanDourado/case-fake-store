# Projeto ETL da Fake Store

## Descrição do Projeto

Este projeto tem como objetivo desenvolver um pipeline ETL (Extract, Transform, Load) que consome dados da [Fake Store API](https://fakestoreapi.com/), transforma-os e persiste as informações em um arquivo Parquet. O foco principal é extrair informações específicas sobre os usuários e seus carrinhos de compras.

## Objetivos do Case

- **Consumir dados de uma API**: Utilizar a Fake Store API para obter dados de usuários, produtos e carrinhos.
- **Transformar os dados**: Processar os dados para extrair informações relevantes e realizar cálculos necessários.
- **Persistir os dados**: Salvar o resultado final em um arquivo Parquet para uso posterior.

### Informações a serem extraídas:

- **Identificador de usuário** (`user_id`).
- **Data mais recente em que o usuário adicionou produtos ao carrinho** (`latest_cart_date`).
- **Categoria em que o usuário tem mais produtos adicionados ao carrinho** (`top_category`).

## Arquitetura da Solução

O pipeline ETL foi construído utilizando o **Apache Airflow**, estruturado em três etapas principais:

1. **Extract**: Extração dos dados dos carrinhos da Fake Store API.
2. **Transform**: Transformação dos dados, enriquecendo-os com informações de produtos e calculando as métricas necessárias.
3. **Load**: Carregamento dos dados transformados em um arquivo Parquet.


## Estrutura do Projeto

```bash
├── dags
│   ├── etl_dag.py          # Definição da DAG do Airflow
│   └── utils
│       ├── extract.py      # Script de extração
│       ├── transform.py    # Script de transformação
│       ├── load.py         # Script de carregamento
│       └── data            # Diretório para arquivos intermediários
│           ├── carts.csv
│           └── transformed_carts.csv
├── plugins                 # Diretório para plugins do Airflow (se necessário)
├── logs                    # Diretório para logs do Airflow
├── requirements.txt        # Dependências do projeto
├── docker-compose.yaml     # Configuração do Docker Compose
├── .env                    # Variáveis de ambiente para o Airflow
└── README.md               # Documentação do projeto
```
![image](https://github.com/user-attachments/assets/03c3a0f9-bc31-4f8d-a2a5-b1c4600fb047)



## Pré-requisitos

- **Docker** e **Docker Compose** instalados.
- **Python 3.7+** instalado (se for executar os scripts localmente).
- Conta no **GitHub** (se for necessário clonar o repositório).

## Configuração do Ambiente

### Clonando o Repositório

```bash
git clone https://github.com/seu_usuario/fake-store-etl.git
cd fake-store-etl
```

### Configurando o Airflow com Docker Compose

O projeto utiliza o Apache Airflow dentro de contêineres Docker para facilitar a implantação e execução do pipeline.

1. **Criar o arquivo `.env`**

   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

   ```env
   AIRFLOW_UID=1000
   ```

   **Nota**: O `AIRFLOW_UID` deve ser o ID do seu usuário no sistema. Você pode obtê-lo executando `id -u` no terminal.

2. **Inicializar o Airflow**

   Inicialize o Airflow e crie as pastas necessárias:

   ```bash
   mkdir -p ./dags ./logs ./plugins
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   ```

3. **Subir os Serviços com Docker Compose**

   ```bash
   docker-compose up -d
   ```

4. **Verificar o Status dos Contêineres**

   ```bash
   docker-compose ps
   ```

5. **Acessar a Interface Web do Airflow**

   Abra o navegador e acesse: [http://localhost:8080](http://localhost:8080)

   - **Usuário:** `admin`
   - **Senha:** `admin`

## Executando o Pipeline ETL

1. **Ativar a DAG**

   Na interface web do Airflow, ative a DAG `fake_store_etl`.

2. **Executar a DAG**

   Você pode executar a DAG manualmente clicando em **"Trigger DAG"** ou aguardar o agendamento automático.

3. **Monitorar as Tasks**

   Acompanhe a execução das tasks `extract`, `transform` e `load` na interface do Airflow.

## Detalhes das Etapas do Pipeline

### 1. Extract

- **Objetivo**: Extrair os dados dos carrinhos da Fake Store API.
- **Script**: `dags/utils/extract.py`
- **Processo**:
  - Faz uma requisição GET para o endpoint `/carts`.
  - Converte a resposta em um DataFrame pandas.
  - Salva os dados em `carts.csv` no diretório `data`.

**Exemplo de Código:**

```python
def extract_cart_data():
    response = requests.get('https://fakestoreapi.com/carts')
    carts = response.json()
    df_carts = pd.DataFrame(carts)
    return df_carts
```

### 2. Transform

- **Objetivo**: Transformar os dados extraídos, enriquecendo-os com informações dos produtos e calculando as métricas necessárias.
- **Script**: `dags/utils/transform.py`
- **Processo**:
  - Lê `carts.csv`.
  - Faz uma requisição GET para o endpoint `/products` para obter detalhes dos produtos.
  - Enriquece os dados dos carrinhos com as categorias dos produtos.
  - Calcula `latest_cart_date` e `top_category` para cada usuário.
  - Salva os dados transformados em `transformed_carts.csv`.

**Exemplo de Código:**

```python
def transform_cart_data(df_carts):
    # Obter dados dos produtos
    response = requests.get('https://fakestoreapi.com/products')
    products = response.json()
    df_products = pd.DataFrame(products)
    # Mapeamento de productId para category
    product_category_mapping = df_products.set_index('id')['category'].to_dict()
    # Transformações adicionais...
    return df_transformed
```

### 3. Load

- **Objetivo**: Carregar os dados transformados em um arquivo Parquet.
- **Script**: `dags/utils/load.py`
- **Processo**:
  - Lê `transformed_carts.csv`.
  - Salva o DataFrame em `user_data.parquet` no diretório `output`.

**Exemplo de Código:**

```python
def load_to_parquet(df_transformed):
    output_dir = '/opt/airflow/dags/utils/output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'user_data.parquet')
    df_transformed.to_parquet(output_path, index=False)
```

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:

```txt
pandas
requests
pyarrow
```

Para instalar as dependências (se estiver executando localmente):

```bash
pip install -r requirements.txt
```

## Configuração do Docker Compose

O arquivo `docker-compose.yaml` define os serviços necessários para executar o Airflow:

- **airflow-webserver**: Interface web do Airflow.
- **airflow-scheduler**: Scheduler que gerencia a execução das DAGs.
- **airflow-worker**: Workers para executar as tasks.
- **postgres**: Banco de dados PostgreSQL para o Airflow.
- **redis**: Backend para a fila de tarefas do Celery.

**Exemplo de Configuração:**

```yaml
version: '3'
services:
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
    # Configurações adicionais...
  redis:
    image: redis:latest
    # Configurações adicionais...
  airflow-webserver:
    image: apache/airflow:2.6.3
    # Configurações adicionais...
```

## Observações Importantes

- **Permissões de Arquivo**: Certifique-se de que o Airflow tem permissão para ler e escrever nos diretórios `dags`, `logs`, `plugins`, `data` e `output`.
- **Configurações do Docker**: Os volumes e mapeamentos de portas estão definidos no `docker-compose.yaml`. Ajuste conforme necessário.
- **Chave Fernet**: A chave Fernet é usada pelo Airflow para criptografar variáveis sensíveis. Certifique-se de defini-la corretamente no arquivo `.env`.

## Possíveis Erros e Soluções

- **Erro de Permissão**: Se encontrar erros de permissão, verifique se os diretórios possuem as permissões corretas.

  ```bash
  sudo chown -R $USER:$USER dags logs plugins
  sudo chmod -R 755 dags logs plugins
  ```

- **Dependências Faltando**: Se receber erros relacionados a módulos não encontrados, verifique se as dependências estão instaladas corretamente.

- **Problemas de Conexão com a API**: Certifique-se de que está conectado à internet e que a API Fake Store está acessível.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

