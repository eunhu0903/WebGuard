from pydantic import BaseModel
from typing import List
from datetime import datetime

class LogEntry(BaseModel):
    site_domain: str
    action: str
    attempted_at: datetime

class LogsUploadRequest(BaseModel):
    logs: List[LogEntry]