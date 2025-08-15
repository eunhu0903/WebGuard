from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from app.db.session import get_db
from app.db.models import Agent
from app.schemas.agent import AgentCreate, AgentResponse, AgentAuth

router = APIRouter()

@router.post("/agent/install", response_model=AgentResponse)
def install_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    agent_uuid = str(uuid.uuid4())
    new_agent = Agent(agent_id=agent_uuid, os=agent.os, version=agent.version)
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent

@router.post("/agent/auth")
def auth_aget(auth: AgentAuth, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.agent_id == auth.agent_id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="등록되지 않은 에이전트 입니다.")
    return {"message": "인증 성공", "agent_id": agent.agent_id}