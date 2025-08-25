from pydantic import BaseModel
from typing import List, Union
from datetime import datetime

class LogEntry(BaseModel):
    site_domain: str
    action: str
    attempted_at: Union[datetime, str]

class LogsUploadRequest(BaseModel):
    logs: List[LogEntry]

class BlockLogCreate(BaseModel):
    agent_id: str
    site_domain: str
    action: str = "blocked"
    attempted_at: datetime