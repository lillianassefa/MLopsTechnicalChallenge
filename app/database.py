from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import psycopg2
import time
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()


db_name = os.getenv('DB_name')
db_user = os.getenv('DB_user')
db_pass = os.getenv('DB_password')
db_host = os.getenv('DB_host')
db_port = os.getenv('DB_port')

logger = logging.getLogger("database")


def db_connection():

    max_retries = 5
    retries = 0
    wait_time = 1

    logger.info(f"Trying to connect to {db_host}:{db_port} as {db_user}...")
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_pass,
                host=db_host,
                port=db_port,
            )
            conn.close()
            logger.info("Connection successful!")
            return
        except Exception as e:
            logger.warning(f"Postgres is not ready yet. Waiting... {str(e)}")
            time.sleep(wait_time)
            retries += 1

DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL)
logger.info("Database engine created")
db_session = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
)

Base = declarative_base()


class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True)
    input_text = Column(String, nullable=False)
    predicted_sentiment = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)


def init_db():
    Base.metadata.create_all(bind=engine)
