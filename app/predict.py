import boto3
from transformers import AutoTokenizer, AutoModelForSequenceClassification,TFAutoModelForSequenceClassification
import os
import zipfile
import logging
from dotenv import load_dotenv
from scipy.special import softmax
import numpy as np

load_dotenv()

# Global variable to hold the loaded model
sentiment_model = None
tokenizer = None
labels = ["Negative", "Neutral", "Positive"] 
logger = logging.getLogger('model')

def download_model_from_s3(bucket_name, s3_object_key, local_model_dir):
    """
    Download the model files from S3 to a local directory and extract them.
    """
    s3_client = boto3.client('s3')
    logger.info("Initializing s3 client")
    try:
        os.makedirs(local_model_dir, exist_ok=True)
        local_zip_path = os.path.join(local_model_dir, 'model.zip')
        s3_client.download_file(bucket_name, s3_object_key, local_zip_path)
        logger.info("downloaded the zip file from s3 successfully")
        # Extract the zip file
        with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
            zip_ref.extractall(local_model_dir)
        logger.info(f"Stored and extracted model to {local_model_dir}")
        return local_model_dir
    except Exception as e:
        logger.error(f"Error downloading and extracting model from S3: {e}")
        return None

def load_model():
    """
    Load the sentiment analysis model.
    """
    global sentiment_model, tokenizer
    try:
        
        bucket_name = os.getenv('bucket_name')
        s3_object_key = os.getenv('object_key')
        local_model_dir = './model'
        # Download the model from S3
        model_path = download_model_from_s3(bucket_name, s3_object_key, local_model_dir)
        if model_path:
            model_full_path = os.path.join(model_path, 'model') 
            # model_full_path = os.path.join(model_path, 'models--cardiffnlp--twitter-roberta-base-sentiment') 
            tokenizer = AutoTokenizer.from_pretrained(model_full_path)
            logger.info("Added the tokenizer successfully")
            sentiment_model= TFAutoModelForSequenceClassification.from_pretrained(model_full_path, from_pt=True)
            logger.info("loaded the model successfully")
    except Exception as e:
        logger.error(f"Error loading model: {e}")

def preprocess(text):
    """
    Preprocess text by replacing user handles and URLs.
    """
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def predict_sentiment(text):
    """
    Predict sentiment for the given text.
    """
    if sentiment_model is None or tokenizer is None:
        load_model()

    if sentiment_model and tokenizer:
        try:
            text = preprocess(text)
            inputs = tokenizer(text, return_tensors='tf', max_length=512, truncation=True)
            output = sentiment_model(**inputs)
            scores = output[0][0].numpy()
            scores = softmax(scores)

            ranking = np.argsort(scores)
            ranking = ranking[::-1]
            top_label = ranking[0]
            sentiment = labels[top_label]
            
            logger.info("Model successfully returned sentiment analysis")
            return sentiment
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return "Error in prediction"
    else:
        return "Model not loaded"


