from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import os
import random

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")


def train_model():
    print(f"Training model {MODEL_VERSION}")
    return {"accuracy": random.uniform(0.75, 0.95)}


def evaluate_model(ti):
    metrics = ti.xcom_pull(task_ids="train_model") or {}
    accuracy = metrics.get("accuracy", 0.8)
    print(f"Model accuracy: {accuracy}")
    ti.xcom_push(key="accuracy", value=accuracy)
    return accuracy


def check_metrics(ti):
    accuracy = ti.xcom_pull(task_ids="evaluate_model", key="accuracy") or 0.0
    return "deploy_model" if accuracy >= 0.80 else "skip_deploy"


def deploy_model():
    print(f"Deploying model {MODEL_VERSION} to production")


with DAG(
    dag_id="ml_retrain_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    train = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
    )

    evaluate = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model,
    )

    check = BranchPythonOperator(
        task_id="check_metrics",
        python_callable=check_metrics,
    )

    deploy = PythonOperator(
        task_id="deploy_model",
        python_callable=deploy_model,
    )

    skip = EmptyOperator(task_id="skip_deploy")

    notify = EmailOperator(
        task_id="notify_success",
        to="mlops-team@example.com",
        subject="Новая модель в продакшене",
        html_content=f"Новая модель <b>{MODEL_VERSION}</b> успешно развернута",
    )

    train >> evaluate >> check >> [deploy, skip]
    deploy >> notify