from pydantic import BaseModel
from typing import Optional, Dict
from enum import Enum

class ContentType(str, Enum):
    email = 'email'
    message = 'message'
    ticket = 'ticket'

class ContentPayload(BaseModel):
    title: Optional[str] = None
    body: str

class AnalyzeRequest(BaseModel):
    content_type: ContentType
    content: ContentPayload
    metadata: Optional[Dict[str, str]] = None

class AnalyzeResponse(BaseModel):
    job_id: str
    status: str
