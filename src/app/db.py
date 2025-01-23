import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DB_HOST = os.getenv("DB_HOST", "34.136.217.207")  # Public IP of the Cloud SQL instance
DB_PORT = os.getenv("DB_PORT", "5432")  # Default PostgreSQL port
DB_NAME = os.getenv("DB_NAME", "default_database_test")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_sqlalchemy_engine():
    """
    Creates and returns a SQLAlchemy engine using the public IP of the database.
    """
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        logging.info("SQLAlchemy engine created.")
        return engine
    except Exception as e:
        logging.error("Error creating SQLAlchemy engine: %s", e)
        raise

# Initialize SQLAlchemy components
engine = get_sqlalchemy_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
