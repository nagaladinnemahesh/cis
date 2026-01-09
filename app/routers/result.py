from fastapi import APIRouter, HTTPException
from app.db.mongo import analysis_collection

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

@router.get("/{job_id}")
def get_analysis(job_id: str):
    job = analysis_collection.find_one(
        {"job_id": job_id},
        {"_id": 0}
    )

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
