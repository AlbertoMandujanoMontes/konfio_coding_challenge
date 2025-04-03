# 🚀 Konfio Coding Challenge

This project provides a complete data engineering and analysis environment using:

- **Apache Airflow** for data pipelines
- **MySQL** as the database
- **Jupyter Notebook** for data analysis and visualization
- **Apache Spark** with optional Apache Iceberg for distributed processing
- **Docker Compose** for reproducibility

---
## 💡 Considerations
- The [`docker-compose.yml`](docker-compose.yml) file includes all the containers required for both the data engineering and data analysis components. This design choice was made to keep the project **self-contained and easy to run**. However, in a real-world application, it would be best practice to **separate these components into distinct environments** to align with deployment, scaling, and security requirements.

- The process that inserts new records into the database will **skip any entry that already exists** for the same `crypto_id` and `date`. This behavior is intentional, as the process is designed to run once per day—after the market closes—to store the final value for each cryptocurrency.

- The pipeline is easily adaptable to track additional cryptocurrencies. To do so, simply add the desired CoinGecko IDs to the `coins_id` list in the operator [`store_cyrpto_values`](dags/crypto_value_data_process.py).

- CoinGecko's API provides data for up to the **last 6 months only**. While the Airflow DAG fetches the most recent data via CoinGecko, **historical data for Q1 2022 was obtained using the `yfinance` package** for analysis purposes. This is done using the script [`load_2022_data.py`](helper_functions/load_2022_data.py)

- The credentials required to access the Airflow UI and MySQL database are included in this repository **for convenience** to facilitate evaluation. However, credentials should always be handled with care and **must never be committed to a public repository** in real-world applications.

- The Spark implementation and analysis workflow are documented in the notebook [`notebooks/Analysis.ipynb`](notebooks/Analysis.ipynb).

- On first run, the MySQL container uses the script [`mysql/init.sql`](mysql/init.sql) to automatically create the required `crypto_currency_value` table. This ensures the environment is ready to receive data without manual setup.

---


## 📦 Project Structure

```
.
├── dags/                     # Airflow DAGs
├── plugins/                 # Custom Airflow operators
├── include/                 # Shared logic (e.g. SQL templates)
├── notebooks/               # Jupyter notebooks for analysis
├── scripts/                 # Optional automation scripts
├── analysis_requirements.txt
├── airflow_requirements.txt
├── docker-compose.yml
└── airflow_settings.yaml    # Connections & variables
```

---

## 🚀 Getting Started

### 1. Clone the project

```bash
git clone https://github.com/AlbertoMandujanoMontes/konfio_coding_challenge.git
cd konfio-coding-challenge
```

### 2. Start the environment

```bash
docker-compose up --build
```

This will spin up:
- Airflow (webserver, scheduler, worker)
- MySQL
- Jupyter Notebook 
- Redis
- PostgreSQL (for Airflow metadata)

---

## 🛠 Services

| Service     | URL                         | Notes                       |
|-------------|-----------------------------|-----------------------------|
| Airflow     | http://localhost:8080       | Username: `admin`, Password: `admin` |
| JupyterLab  | http://localhost:8888       | No token/password required  |
| MySQL       | localhost:3306              | User: `dev_user`, Password: `dev_pass` |

---

## 📊 Data Analysis

The `notebooks/Analysis.ipynb` notebook connects to the MySQL container, retrieves crypto value data, and calculates a 5-day moving average using **PySpark**. The results can be plotted or persisted using **Apache Iceberg**.

---

## 🧪 Airflow Pipelines

The DAG `crypto_value_data_process` fetches and stores cryptocurrency data using a custom operator. Connections and variables are preloaded from `airflow_settings.yaml`.

---

## 🧹 Requirements

- `analysis_requirements.txt`: for Jupyter dependencies
- `airflow_requirements.txt`: for DAG and plugin dependencies

These are auto-installed when the containers start.


## 🧼 Cleanup

To remove all containers and volumes:

```bash
docker-compose down -v
```