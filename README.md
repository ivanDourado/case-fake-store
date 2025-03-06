# Fake Store ETL Project

<h6>Don't speak english? <a href="https://github.com/ivanDourado/case-fake-store/blob/master/README-ptbr.md">Clique Aqui</a> para visualizar essa página em português.</h6>

## Project Description

This project aims to develop an ETL (Extract, Transform, Load) pipeline that fetches data from the [Fake Store API](https://fakestoreapi.com/), processes it, and stores the transformed information in a Parquet file. The primary focus is to extract specific details about users and their shopping carts.

## Case Objectives

- **Consume API data**: Fetch data from the Fake Store API, including users, products, and shopping carts.
- **Transform the data**: Process and enrich the extracted data, performing necessary calculations.
- **Persist the data**: Save the final processed data in a Parquet file for further use.

### Extracted Information:

- **User ID** (`user_id`)
- **Most recent date the user added products to their cart** (`latest_cart_date`)
- **Category with the most products added by the user** (`top_category`)

## Solution Architecture

The ETL pipeline is built using **Apache Airflow**, structured into three main steps:

1. **Extract**: Fetch shopping cart data from the Fake Store API.
2. **Transform**: Enrich the data with product details and compute required metrics.
3. **Load**: Save the processed data into a Parquet file.

## Project Structure

```bash
├── dags
│   ├── etl_dag.py          # Airflow DAG definition
│   └── utils
│       ├── extract.py      # Extraction script
│       ├── transform.py    # Transformation script
│       ├── load.py         # Loading script
│       └── data            # Directory for intermediate files
│           ├── carts.csv
│           └── transformed_carts.csv
├── plugins                 # Airflow plugins directory (if needed)
├── logs                    # Airflow logs directory
├── requirements.txt        # Project dependencies
├── docker-compose.yaml     # Docker Compose configuration
├── .env                    # Airflow environment variables
└── README.md               # Project documentation
```
![image](https://github.com/user-attachments/assets/a3f94242-820a-43da-ba7c-3a782cda1897)


## Prerequisites

- **Docker** and **Docker Compose** installed.
- **Python 3.7+** installed (if running scripts locally).
- **GitHub account** (if cloning the repository).

## Environment Setup

### Clone the Repository

```bash
git clone https://github.com/your_user/fake-store-etl.git
cd fake-store-etl
```

### Configure Airflow with Docker Compose

The project runs Apache Airflow in Docker containers for easy deployment and execution.

1. **Create the `.env` file**

   Create a `.env` file in the project root with the following content:

   ```env
   AIRFLOW_UID=1000
   ```

   **Note**: The `AIRFLOW_UID` should match your system user ID. You can get it by running `id -u` in the terminal.

2. **Initialize Airflow**

   ```bash
   mkdir -p ./dags ./logs ./plugins
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   ```

3. **Start the Services with Docker Compose**

   ```bash
   docker-compose up -d
   ```

4. **Check Container Status**

   ```bash
   docker-compose ps
   ```

5. **Access Airflow Web Interface**

   Open your browser and go to: [http://localhost:8080](http://localhost:8080)

   - **Username:** `admin`
   - **Password:** `admin`

## Running the ETL Pipeline

1. **Enable the DAG**

   In the Airflow web interface, activate the `fake_store_etl` DAG.

2. **Trigger the DAG**

   Run the DAG manually by clicking **"Trigger DAG"** or wait for automatic scheduling.

3. **Monitor the Tasks**

   Track the execution of the `extract`, `transform`, and `load` tasks in Airflow.

## ETL Pipeline Steps

### 1. Extract

- **Objective**: Fetch shopping cart data from the Fake Store API.
- **Script**: `dags/utils/extract.py`
- **Process**:
  - Perform a GET request to the `/carts` endpoint.
  - Convert the response into a pandas DataFrame.
  - Save the data in `carts.csv` inside the `data` directory.

**Example Code:**

```python
def extract_cart_data():
    response = requests.get('https://fakestoreapi.com/carts')
    carts = response.json()
    df_carts = pd.DataFrame(carts)
    return df_carts
```

### 2. Transform

- **Objective**: Enrich cart data with product details and compute necessary metrics.
- **Script**: `dags/utils/transform.py`
- **Process**:
  - Read `carts.csv`.
  - Fetch product details from the `/products` endpoint.
  - Enrich cart data with product categories.
  - Calculate `latest_cart_date` and `top_category` per user.
  - Save the transformed data in `transformed_carts.csv`.

**Example Code:**

```python
def transform_cart_data(df_carts):
    response = requests.get('https://fakestoreapi.com/products')
    products = response.json()
    df_products = pd.DataFrame(products)
    
    product_category_mapping = df_products.set_index('id')['category'].to_dict()
    
    # Additional transformations...
    return df_transformed
```

### 3. Load

- **Objective**: Save the transformed data as a Parquet file.
- **Script**: `dags/utils/load.py`
- **Process**:
  - Read `transformed_carts.csv`.
  - Save the DataFrame as `user_data.parquet` inside the `output` directory.

**Example Code:**

```python
def load_to_parquet(df_transformed):
    output_dir = '/opt/airflow/dags/utils/output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'user_data.parquet')
    df_transformed.to_parquet(output_path, index=False)
```

## Dependencies

The project dependencies are listed in `requirements.txt`:

```txt
pandas
requests
pyarrow
```

To install dependencies (if running locally):

```bash
pip install -r requirements.txt
```

## Docker Compose Configuration

The `docker-compose.yaml` file defines the required services:

- **airflow-webserver**: Airflow's web interface.
- **airflow-scheduler**: Schedules DAG execution.
- **airflow-worker**: Executes tasks.
- **postgres**: Airflow's PostgreSQL database.
- **redis**: Celery's task queue backend.

## Common Issues and Solutions

- **Permission Errors**:

  ```bash
  sudo chown -R $USER:$USER dags logs plugins
  sudo chmod -R 755 dags logs plugins
  ```

- **Missing Dependencies**: Ensure all dependencies are installed properly.
- **API Connection Issues**: Check internet connection and API availability.

## Contributing

Contributions are welcome! Feel free to open issues and pull requests.

---

This documentation provides a comprehensive guide for users and contributors to understand, set up, and run the ETL pipeline efficiently. 🚀
