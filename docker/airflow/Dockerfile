FROM apache/airflow:2.9.2

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow
COPY airflow_requirements.txt /requirements-extra.txt
RUN pip install --no-cache-dir -r /requirements-extra.txt

