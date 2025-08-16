from pydantic import BaseModel
from typing import List, Union
from datetime import datetime

class LogEntry(BaseModel):
    site_domain: str
    action: str
    attempted_at: Union[datetime, str]

class LogsUploadRequest(BaseModel):
    logs: List[LogEntry]