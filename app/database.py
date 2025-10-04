from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite DB (fichier local)
DATABASE_URL = "sqlite:///./ecole.db"

# connect_args={"check_same_thread": False} est requis pour SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
