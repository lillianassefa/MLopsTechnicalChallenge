from fastapi.testclient import TestClient
import main  
from unittest.mock import patch


client = TestClient(main)

def test_read_main():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


@patch('app/predict.py')  
def test_predict_api(mock_predict):
    mock_predict.return_value = "Positive"
    response = client.get("/predict?text=I love sunny days")
    assert response.status_code == 200
    assert response.json() == {"text": "I love sunny days", "sentiment": "Positive"}
