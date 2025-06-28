import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def get_engine(db_name):
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{db_name}"
    return create_engine(DATABASE_URL, echo=False)

# Engines for each DB
engine_pet = get_engine(os.getenv("PET_DB_NAME"))
engine_post = get_engine(os.getenv("POST_DB_NAME"))
engine_reactions = get_engine(os.getenv("REACTIONS_DB_NAME"))

# Sessions
SessionPet = sessionmaker(autocommit=False, autoflush=False, bind=engine_pet)
SessionPost = sessionmaker(autocommit=False, autoflush=False, bind=engine_post)
SessionReactions = sessionmaker(autocommit=False, autoflush=False, bind=engine_reactions)

Base = declarative_base()
