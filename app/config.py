from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_name : str
    DB_user: str
    DB_password : str
    DB_host : str
    DB_port : str
    AWS_access_key_id : str
    AWS_secret_access_key : str
    bucket_name: str
    model_file_name: str
    object_key :str
    
    class Config:
        env_file:str =  '.env'


@lru_cache
def getSettings() -> Settings:
    return Settings()


