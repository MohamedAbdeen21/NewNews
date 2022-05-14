from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from xmlscraper.xmlscraper.spiders.xmlscrape import run
from xmlscraper import extract_to_csv

with DAG(dag_id = "airflow_dag",
        start_date = datetime(2022,5,11),
        schedule_interval = "10 0 * * *",
        catchup=False) as dag:
    scrape_and_load = PythonOperator(task_id = "scrapy", python_callable=run)
    create_csv = PythonOperator(task_id = "create_csv", python_callable=extract_to_csv.run)

    scrape_and_load >> create_csv 
