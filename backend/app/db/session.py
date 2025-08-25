from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine_mysql = create_engine(settings.MYSQL_DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocalMySQL = sessionmaker(autocommit = False, autoflush=False, bind=engine_mysql)

engine_pg = create_engine(settings.POSTGRES_DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocalPG = sessionmaker(autocommit=False, autoflush=False, bind=engine_pg)

Base = declarative_base()

def get_db_mysql():
    db = SessionLocalMySQL()
    try:
        yield db
    finally:
        db.close()

def get_db_pg():
    db = SessionLocalPG()
    try:
        yield db
    finally:
        db.close()