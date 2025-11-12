SHELL := /bin/bash

.PHONY: help init compose-up compose-down airflow-producer streamlit notebook lint

help:
	@echo "Available commands:"
	@echo "  make init           Install Python dependencies (virtualenv recommended)"
	@echo "  make compose-up     Start Docker services (Kafka, Postgres, Airflow)"
	@echo "  make compose-down   Stop Docker services"
	@echo "  make producer       Run the Kafka producer locally"
	@echo "  make streamlit      Launch the Streamlit dashboard"
	@echo "  make notebook       Start Jupyter Lab for exploration"
	@echo "  make lint           Run basic formatting & static checks"

init:
	pip install --upgrade pip
	pip install -r requirements.txt

compose-up:
	docker compose up -d

compose-down:
	docker compose down --remove-orphans

producer:
	python producer/producer.py --rows 1000 --rate 100 --topic transactions --bootstrap-server localhost:29092

streamlit:
	streamlit run analytics/streamlit_dashboard.py

notebook:
	jupyter lab notebooks

lint:
	python -m compileall producer consumers analytics scripts

