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

app = FastAPI(
    title="Globant Big Data Migration",
    description="API for data migration, backup, and restoration.",
    version="1.0.0"
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Validate environment variables
@app.on_event("startup")
async def validate_env_variables():
    required_envs = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing_envs = [var for var in required_envs if not os.getenv(var)]
    if missing_envs:
        logging.error(f"Missing required environment variables: {missing_envs}")
        raise RuntimeError(f"Missing required environment variables: {missing_envs}")
    logging.info("All required environment variables are set.")

# Startup health check
@app.on_event("startup")
async def startup_event():
    try:
        with engine.connect() as connection:
            logging.info("Database connection is healthy.")
    except Exception as e:
        logging.error("Database connection failed: %s", e)
        raise

# Shutdown hook
@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Application is shutting down.")

# Routes for loading CSV data
@app.post("/load_csv/")
def load_csv_data(employees_file: str = None, departments_file: str = None, jobs_file: str = None, db: Session = Depends(get_db)):
    logging.info("Load CSV request received.")
    if departments_file:
        logging.info(f"Loading departments from {departments_file}.")
        utils.load_csv_departments(departments_file, db)
    if jobs_file:
        logging.info(f"Loading jobs from {jobs_file}.")
        utils.load_csv_jobs(jobs_file, db)
    if employees_file:
        logging.info(f"Loading employees from {employees_file}.")
        utils.loa
