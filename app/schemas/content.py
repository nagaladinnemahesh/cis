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

# ai draft for reply with coffer
class ReplyDraftContent(BaseModel):
    original_subject: str
    original_body: str
    from_email: Optional[str] = None

class AnalyzeRequest(BaseModel):
    content_type: ContentType
    content: ContentPayload
    metadata: Optional[Dict[str, str]] = None

class AnalyzeResponse(BaseModel):
    job_id: str
    status: str
