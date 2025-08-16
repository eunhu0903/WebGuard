from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(String(64), unique=True, nullable=False, index=True)
    token = Column(String(128), unique=True, nullable=False)
    os = Column(String(50), nullable=False)
    version = Column(String(20), nullable=False)
    installed_at = Column(DateTime(timezone=True), server_default=func.now())