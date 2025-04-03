# 🚀 Konfio Coding Challenge

This project provides a complete data engineering and analysis environment using:

- **Apache Airflow** for data pipelines
- **MySQL** as the database
- **Jupyter Notebook** for data analysis and visualization
- **Apache Spark** with optional Apache Iceberg for distributed processing
- **Docker Compose** for reproducibility

---
## 📦 Considerations
- The process to insert new registers in the database will not insert the data if there is already a register with the same same crypto_id and date. This is because the process is intended to run once the day is over and we have the close value of the crypto. 
- The process can be adapted to get the value of more cryptocurrencies its just a matter of adding the id into the list "coins_id". 
- The CoinGecko only allows to get information of the last 6 months, the Airflow process uses it to get the up to date data, but for the analysis of the data of the first quarter of 2022 the package yfinance was used.
- The credentials necessary to to access the Airflow UI and the MySQL database are provided in this page for convinance sake to make the evaluation of the project easier. Credentials should be handled with extreme care and under any circumstance should be uploaded to a public repository. 
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
git clone https://github.com/your-org/konfio-coding-challenge.git
cd konfio-coding-challenge
```

### 2. Start the environment

```bash
docker-compose up --build
```

This will spin up:
- Airflow (webserver, scheduler, worker)
- MySQL
- Jupyter Notebook (http://localhost:8888)
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

---

## 📬 Questions?

Open an issue or reach out to the team!
