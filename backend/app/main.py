from fastapi import FastAPI
from app.db.models import Base
from app.db.session import engine
from app.api import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)