import uuid
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Agent
from app.schemas.agent import AgentCreate, AgentResponse, AgentAuth
from app.api.dependencies import verify_agent

router = APIRouter()

@router.post("/agent/install", response_model=AgentResponse)
def install_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    agent_uuid = str(uuid.uuid4())
    token = secrets.token_hex(32)

    new_agent = Agent(agent_id=agent_uuid, os=agent.os, version=agent.version, token=token)
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent

@router.post("/agent/auth")
def auth_aget(agent: Agent = Depends(verify_agent)):
    return {"message": "인증 성공", "agent_id": agent.agent_id}