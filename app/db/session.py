from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from fastapi import Depends
from typing import Annotated
from dotenv import load_dotenv
from pathlib import Path

# Load the project-level .env file. Environment variables supplied by the
# operating system still take precedence because load_dotenv does not override
# existing values by default.




PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / '.env')


DB_URL = os.getenv('DB_URL')
if not DB_URL:
    raise RuntimeError(
        f'DB_URL is not configured.'
        'or in the process environment.'
    )

# Neon may close idle pooled connections. Check a connection before using it
# and recycle connections periodically so requests do not receive a stale one.
engine = create_engine(
    DB_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependancy = Annotated[Session, Depends(get_db)]
