from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

def SessionLocal():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return maker()
