from pydantic import BaseModel
from datetime import datetime

class AgentCreate(BaseModel):
    os: str
    version: str

class AgentResponse(BaseModel):
    agent_id: str
    os: str
    version: str
    installed_at: datetime
    token: str

    class Config:
        from_attributes = True

class AgentAuth(BaseModel):
    agent_id: str
    token: str