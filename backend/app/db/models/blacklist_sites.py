from sqlalchemy import Column, BigInteger, String, Enum, DateTime
from datetime import datetime
from app.db.session import Base

class BlacklistSite(Base):
    __tablename__ = "blacklist_sites"

    id = Column(BigInteger, primary_key=True, index=True)
    domain = Column(String(255), nullable=False, index=True)
    category = Column(Enum('phishing', 'gambling', 'porn', 'etc', name='site_category'), nullable=False)
    source = Column(String(50), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)