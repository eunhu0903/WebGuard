from fastapi import HTTPException, status, Header, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Agent

def verify_agent(agent_id: str = Header(...), token: str = Header(...), db: Session = Depends(get_db)) -> Agent:
    agent = db.query(Agent).filter(Agent.agent_id == agent_id, Agent.token == token).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="등록되지 않은 Agent이거나 토큰이 잘못되었습니다."
        )
    return agent
