from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

url_tokens = {
    "DB_USER": os.getenv("DB_USER", ""),
    "DB_PASS": os.getenv("DB_PASS", ""),
    "DB_HOST": os.getenv("DB_HOST", ""),
    "DB_NAME": os.getenv("DB_NAME", "")
}

if not all(url_tokens.values()):
    raise ValueError("Database connection parameters are not fully set in the environment variables.")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{url_tokens['DB_USER']}:{url_tokens['DB_PASS']}@"
    f"{url_tokens['DB_HOST']}/{url_tokens['DB_NAME']}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_database():
    Base.metadata.create_all(bind=engine)
