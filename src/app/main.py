import os
import logging
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from . import models, schemas, crud, utils, backup
from .routers import metrics

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Globant Big Data Migration")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check on startup to verify the database connection
@app.on_event("startup")
async def startup_event():
    try:
        with engine.connect() as connection:
            logging.info("Database connection is healthy.")
    except Exception as e:
        logging.error("Database connection failed: %s", e)
        raise

# Routes for loading CSV data
@app.post("/load_csv/")
def load_csv_data(employees_file: str = None, departments_file: str = None, jobs_file: str = None, db: Session = Depends(get_db)):
    if departments_file:
        utils.load_csv_departments(departments_file, db)
    if jobs_file:
        utils.load_csv_jobs(jobs_file, db)
    if employees_file:
        utils.load_csv_employees(employees_file, db)
    return {"status": "CSV data loaded successfully"}

# Routes for inserting data
@app.post("/insert_data/")
def insert_data(employees: list[schemas.EmployeeCreate] = None, departments: list[schemas.DepartmentCreate] = None, jobs: list[schemas.JobCreate] = None, db: Session = Depends(get_db)):
    if departments:
        for dept in departments:
            crud.create_department(db, dept)
    if jobs:
        for job in jobs:
            crud.create_job(db, job)
    if employees:
        for emp in employees:
            crud.create_employee(db, emp)
    return {"status": "Data inserted successfully"}

# Backup and restore routes
@app.post("/backup/{table_name}")
def backup_data(table_name: str):
    result = backup.backup_table(table_name)
    return {"message": result}

@app.post("/restore/{table_name}")
def restore_data(table_name: str):
    result = backup.restore_table(table_name)
    return {"message": result}

# Metrics router
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
