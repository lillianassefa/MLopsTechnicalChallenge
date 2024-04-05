# MLopsTechnicalChallenge
This project is initially built for a technical challenge to join Junior MLOPS Postion

# FastAPI Sentiment Analysis Service

It is a sentiment analysis service built with FastAPI. It utilizes a machine learning model(ROBERTA) to analyze text and determine sentiment (Positive, Negative, Neutral). The service is containerized using Docker for easy deployment and scalability.

## Features

- Sentiment analysis of textual data.
- RESTful API endpoint.
- Integration with RDS(PostgreSQL) database for logging predictions.
- Docker support for easy deployment.

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.12+
- Docker
- PostgreSQL (For local testing or if not using AWS RDS)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lillianassefa/MLopsTechnicalChallenge.git
   cd MLopsTechnicalChallenge/app

2. **Set up a virtual environment (Optional but recommended):**

   `python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`   `

3. **Install Dependencies:**

   `pip install -r requirements.txt`

4. **Set Environment Variable**

   Set up the following environment variables, either in a .env file or in   your environment:
    DB_NAME: postgres
    DB_USER: postgres
    DB_PASSWORD: Database password
    DB_HOST: microservicemodel.crwuq2iiy62m.us-east-1.rds.amazonaws.com
    DB_PORT: 5432
    AWS_ACCESS_KEY_ID: AWS access key
    AWS_SECRET_ACCESS_KEY: AWS secret access key
    BUCKET_NAME: modelforpredict

5. **Running the application locally**

   `uvicorn main:app --reload`

## Running with docker

1. **Build docker image**
   `docker build -t microservicesentimentpredict`

2. **Run docker container**

   `docker run -d -p 8000:8000 fastapi-sentiment-app`

# Usage

There is one api endpoint which is /predict which is used to accept text input from user and outputs the sentiment value.

### API Endpoints
GET /ping: Health check endpoint.
POST /predict: Endpoint to submit text for sentiment analysis.
Request body format:

`{"text": "Your sample text here"}`

### Testing 

The application can be tested using Postman or the Swagger UI at http://localhost:8000/docs.


### Contributing
Please feel free to contribute to this project and give suggestions


## License
This project is licensed under the MIT License - see the LICENSE.md file for details.