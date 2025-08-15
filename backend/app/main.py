from fastapi import FastAPI
from app.db.models import Base
from app.db.session import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)