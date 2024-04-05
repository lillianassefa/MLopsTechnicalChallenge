from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import uvicorn
from predict import predict_sentiment
import os
import logging
from logging.handlers import RotatingFileHandler
from database import init_db, PredictionLog, db_session
from pydantic import BaseModel

if not os.path.exists("logs"):
    os.makedirs("logs")

loggers = {
    "default": "logs/app.log",
    "database": "logs/database.log",
    "requests": "logs/requests.log",
    "model": "logs/model.log",
}

# create and configure logging for different functions

for logger_name, log_file in loggers.items():

    file_handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)


logger = logging.getLogger("requests")  # logging for api application status
db_logger = logging.getLogger("database")  # logging for database status


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


class PredictRequest(BaseModel):
    text: str


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()
    db_logger.info("Database created Successfully")


def log_prediction(db: Session, text: str, sentiment: str):
    log_entry = PredictionLog(input_text=text, predicted_sentiment=sentiment)
    logger.info(f"Logged request ${text} and response ${sentiment}")
    db_logger.info(f"Added request ${text} and response ${sentiment} to database")
    db.add(log_entry)
    db.commit()


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.post("/predict")
def predict(request: PredictRequest, db: Session = Depends(get_db)):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided for prediction.")
    sentiment = predict_sentiment(request.text)
    log_prediction(db, request.text, sentiment)
    return {"text": request.text, "sentiment": sentiment}


if __name__ == "__main__":
    logger.info("Starting FastAPI application")
    uvicorn.run("app:app", host="0.0.0.0", port="8080", reload=True)
    logger.info("Application started successfully")
