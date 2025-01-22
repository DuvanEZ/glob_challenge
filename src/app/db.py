import os
import logging
from google.cloud.sql.connector import Connector, IPTypes
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración
DATABASE_NAME = os.getenv("DB_NAME", "default_database")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME", "project:region:instance")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
IP_TYPE = IPTypes.PUBLIC  # Cambiar a IPTypes.PRIVATE si usas IP privada

# Inicializa el conector
connector = Connector(ip_type=IP_TYPE)

def get_connection():
    """
    Retorna una conexión de psycopg2 a PostgreSQL usando Cloud SQL Auth Proxy.
    """
    try:
        conn = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "psycopg2",
            user=DB_USER,
            password=DB_PASSWORD,
            db=DATABASE_NAME
        )
        logging.info("Conexión a la base de datos PostgreSQL establecida.")
        return conn
    except Exception as e:
        logging.error("Error al conectar a la base de datos: %s", e)
        raise

# SQLAlchemy setup
def get_sqlalchemy_engine():
    """
    Crea un motor de SQLAlchemy con el conector de Google Cloud SQL.
    """
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DATABASE_NAME}?host=/cloudsql/{INSTANCE_CONNECTION_NAME}"
    )
    return engine

engine = get_sqlalchemy_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
