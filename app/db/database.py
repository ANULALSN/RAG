from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# --------------------------------------------------
# Database location
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_PATH = DATA_DIR / "rag.db"

DATABASE_URL = (
    f"sqlite:///{DATABASE_PATH}"
)


# --------------------------------------------------
# SQLAlchemy engine
# --------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


# --------------------------------------------------
# Base model
# --------------------------------------------------

class Base(DeclarativeBase):
    pass


# --------------------------------------------------
# Session factory
# --------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# --------------------------------------------------
# Database session dependency
# --------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
def init_db():
    from app.db import models

    Base.metadata.create_all(
        bind=engine
    )