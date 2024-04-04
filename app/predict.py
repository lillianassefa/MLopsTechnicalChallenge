import boto3
from transformers import RobertaTokenizer, RobertaForSequenceClassification, pipeline
import os
import zipfile
import logging

from config import getSettings
settings = getSettings()

# Global variable to hold the loaded model
sentiment_model = None
tokenizer = None

logger = logging.getLogger('model')

def download_model_from_s3(bucket_name, s3_object_key, local_model_dir):
    """
    Download the model files from S3 to a local directory and extract them.
    """
    s3_client = boto3.client('s3')
    try:
        os.makedirs(local_model_dir, exist_ok=True)
        local_zip_path = os.path.join(local_model_dir, 'model.zip')
        s3_client.download_file(bucket_name, s3_object_key, local_zip_path)

        # Extract the zip file
        with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
            zip_ref.extractall(local_model_dir)

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
        
        bucket_name = settings.bucket_name
        s3_object_key = settings.object_key
        local_model_dir = './model'

        # Download the model from S3
        model_path = download_model_from_s3(bucket_name, s3_object_key, local_model_dir)
        if model_path:
            model_full_path = os.path.join(model_path, 'sentiment model') 

            tokenizer = RobertaTokenizer.from_pretrained(model_full_path)
            sentiment_model= RobertaForSequenceClassification.from_pretrained(model_full_path)
    except Exception as e:
        logger.error(f"Error loading model: {e}")

def predict_sentiment(text):
    """
    Predict sentiment for the given text.
    """
    if sentiment_model is None or tokenizer is None:
        load_model()

    if sentiment_model and tokenizer:
        try:
            inputs = tokenizer(text, return_tenson = 'pt', max_length= 512, truncation = True)
            result = sentiment_model(**inputs)
            sentiment_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
            sentiment = sentiment_map.get(result[0]['label'], "Unknown")
            return sentiment
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return "Error in prediction"
    else:
        return "Model not loaded"


