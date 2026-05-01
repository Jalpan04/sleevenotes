from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# We default to local SQLite for immediate development without blocking.
# When you make a Neon.tech or Supabase account, you just set DATABASE_URL in your environment!
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend.db")

# SQLite needs check_same_thread=False, Postgres does not.
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
