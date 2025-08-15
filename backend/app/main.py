from fastapi import FastAPI
from app.db.models import Base
from app.db.session import engine
from app.api import auth, agent, policy, logs

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(agent.router)
app.include_router(policy.router)
app.include_router(logs.router)