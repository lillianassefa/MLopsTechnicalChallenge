from database import db_connection
import os
from dotenv import load_dotenv

load_dotenv()


db_name = os.getenv('DB_name')
db_user = os.getenv('DB_user')
db_pass = os.getenv('DB_password')
db_host = os.getenv('DB_host')
db_port = os.getenv('DB_port')

def test_database_connection():

    test_db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    assert db_connection(test_db_url) is not None
