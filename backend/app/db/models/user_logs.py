from sqlalchemy import Column, BigInteger, ForeignKey, Enum, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.db.session import Base

class UserLog(Base):
    __tablename__ = "user_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    site_id = Column(BigInteger, ForeignKey("blacklist_sites.id"), nullable=False)
    attempted_at = Column(DateTime, default=datetime.utcnow)
    action = Column(Enum('blocked', 'warned', name="log_action"), nullable=False)

    user = relationship("User", backref="logs")
    site = relationship("BlacklistSite", backref="logs")