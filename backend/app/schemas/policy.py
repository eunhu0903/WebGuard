from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class BlacklistSiteResponse(BaseModel):
    domain: str
    category: str
    source: str
    added_at: Optional[datetime]

class BlacklistResponse(BaseModel):
    sites: List[BlacklistSiteResponse]

    class Config:
        from_attributes = True