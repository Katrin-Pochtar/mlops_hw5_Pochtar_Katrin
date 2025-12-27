# MLOps HW5 — Airflow DAG with Model Deployment Notification

## Overview
DAG that trains a model, evaluates metrics, deploys conditionally, and sends email notification on success.

## Tasks
- `train_model` — simulates training, returns accuracy
- `evaluate_model` — extracts and logs accuracy
- `check_metrics` — branches based on threshold (deploy or skip)
- `deploy_model` — simulates production deployment
- `notify_success` — sends email with model version
- `skip_deploy` — no-op when metrics fail

## Configuration
```bash
export MODEL_VERSION="v2.3.1"
export ACCURACY_THRESHOLD="0.80"
```

## Quick Start
```bash
source .venv/bin/activate
export AIRFLOW_HOME="$PWD/airflow"
export MODEL_VERSION="v2.3.1"
airflow standalone
```

Access UI: http://localhost:8080

## Email Setup (SMTP)
Create connection in Airflow UI:
- **Admin → Connections → +**
- **Connection Id:** `smtp_default`
- **Type:** SMTP
- **Host:** `smtp.gmail.com`
- **Port:** `587`
- **Login:** your_email@gmail.com
- **Password:** your_app_password

For Gmail App Password: https://myaccount.google.com/apppasswords

## Files
- `airflow/dags/ml_retrain_pipeline.py` — DAG code
- `screenshots/airflow_run_success.png` — successful run
