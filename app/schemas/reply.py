from pydantic import BaseModel, Field
from typing import Dict, Optional

class OriginalEmail(BaseModel):
    from_: str = Field(..., alias = "from")
    subject: str
    body: str

    class Config:
        fields = {"from_": "from"}  # handle reserved keyword


class EmailAnalysis(BaseModel):
    intent: str
    urgency: str
    summary: str


class ReplyContext(BaseModel):
    tone: str
    user_intent: str


class ReplyDraftContent(BaseModel):
    original_email: OriginalEmail
    analysis: EmailAnalysis
    context: ReplyContext


class ReplyDraftRequest(BaseModel):
    content_type: str  # must be "email_reply"
    content: ReplyDraftContent
    metadata: Optional[Dict] = {}
