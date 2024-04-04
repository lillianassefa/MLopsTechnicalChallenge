from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import uvicorn
from predict import predict_sentiment
import os
import logging
from logging.handlers import RotatingFileHandler
import boto3
import psycopg2
from psycopg2 import sql
from database import db_session, engine, Base, init_db, PredictionLog
import boto3
from config import getSettings

settings = getSettings()

loggers = {
    'default':  'app.log',
    'database': 'database.log',
    'requests': 'requests.log',
    'model': 'model.log'
}

#create and configure logging for different functions

for logger_name, log_file in loggers.items():
   
    file_handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)

    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  
    logger.addHandler(file_handler)


logger = logging.getLogger('default')   # logging for application
db_logger = logging.getLogger('database')      # logging for database


def get_db():
    db=db_session()
    try :
        yield db
    finally: 
        db.close()


app = FastAPI()
@app.on_event("startup")
def on_startup():
    init_db()
    db_logger.info("Database created Successfully")

def log_prediction(db: Session, text: str, sentiment: str):
    log_entry = PredictionLog(input_text = text, predicted_sentiment= sentiment)
    db.add(log_entry)
    db.commit()

@app.get("/ping")
def pong():
    return {"ping": "pong!"}

@app.get("/predict")
def predict(text: str, db: Session = Depends(db_session)):
    if not text:
        raise HTTPException(status_code=400, detail="No text provided for prediction.")
    sentiment = predict_sentiment(text)
    log_prediction(db, text, sentiment)
    return {"text": text, "sentiment": sentiment}



if __name__ == "__main__" :
    logger.info("Starting FastAPI application")
    uvicorn.run('app:app',host='0.0.0.0', port= '8080', reload=True)
