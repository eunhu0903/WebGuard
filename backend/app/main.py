from fastapi import FastAPI
from app.db.models import Base
from app.db.session import engine
from app.api import auth, agent

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(agent.router)