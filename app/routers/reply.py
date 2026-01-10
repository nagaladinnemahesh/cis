from fastapi import APIRouter, BackgroundTasks
from app.schemas.reply import ReplyDraftRequest
from app.workers.processor import process_analysis_job
import uuid

router = APIRouter(prefix="/reply", tags=["reply"])

@router.post("/draft")
def create_reply_draft(
    payload: ReplyDraftRequest,
    background_tasks: BackgroundTasks
):
    job_id = f"cis_{uuid.uuid4().hex[:8]}"

    # store job
    from app.db.mongo import analysis_collection
    analysis_collection.insert_one({
        "job_id": job_id,
        "status": "pending",
        "content_type": payload.content_type,
        "content": payload.content.dict(),
        "metadata": payload.metadata
    })

    background_tasks.add_task(process_analysis_job, job_id)

    return {
        "job_id": job_id,
        "status": "pending"
    }
