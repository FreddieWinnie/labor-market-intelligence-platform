from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    AZDUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
    AZDUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")