# Globant Big Data Migration PoC

This repository demonstrates how to:
1. Load historical data from CSV into a new **PostgreSQL** database on **Cloud SQL**.
2. Provide a **FastAPI** service to receive new data (batch inserts).
3. Backup/restore tables in **Avro** format.
4. Retrieve metrics (Challenge #2).

## Prerequisites
1. A GCP project with **Cloud Run**, **Cloud Build**, and **Cloud SQL** enabled.
2. A Cloud SQL PostgreSQL instance.
3. A service account with necessary permissions.

## Usage
See `src/app/main.py` for available endpoints. Use `/docs` to interact via Swagger UI.
