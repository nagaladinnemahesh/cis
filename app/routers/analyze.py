import uuid
from fastapi import APIRouter
from app.schemas.content import AnalyzeRequest, AnalyzeResponse
from app.db.mongo import analysis_collection

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)

@router.post("/", response_model=AnalyzeResponse)
def analyze_content(request: AnalyzeRequest):
    job_id = "cis_" + uuid.uuid4().hex[:8]

    analysis_collection.insert_one({
        "job_id": job_id,
        "status": "pending",
        "content_type": request.content_type,
        "content": request.content.dict(),
        "metadata": request.metadata,
        "result": None
    })

    return AnalyzeResponse(
        job_id=job_id,
        status="pending"
    )
