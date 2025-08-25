from fastapi import FastAPI
from app.db.models import Base as BaseMySQL
from app.db.models import Base as BasePG
from app.db.session import engine_mysql, engine_pg
from app.api import auth, agent, policy, logs, sync_api

app = FastAPI()

BaseMySQL.metadata.create_all(bind=engine_mysql)
BasePG.metadata.create_all(bind=engine_pg)

app.include_router(auth.router)
app.include_router(agent.router)
app.include_router(policy.router)
app.include_router(logs.router)
app.include_router(sync_api.router)
