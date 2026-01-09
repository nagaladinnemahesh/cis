import uuid
from fastapi import APIRouter, BackgroundTasks
from app.schemas.content import AnalyzeRequest, AnalyzeResponse
from app.db.mongo import analysis_collection
from app.workers.processor import process_analysis_job

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)

@router.post("/", response_model=AnalyzeResponse)
def analyze_content(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    job_id = "cis_" + uuid.uuid4().hex[:8]

    analysis_collection.insert_one({
        "job_id": job_id,
        "status": "pending",
        "content_type": request.content_type,
        "content": request.content.dict(),
        "metadata": request.metadata,
        "result": None
    })

    # trigger background processing
    background_tasks.add_task(process_analysis_job, job_id)

    return AnalyzeResponse(
        job_id=job_id,
        status="pending"
    )
