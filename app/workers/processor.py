import time
from app.db.mongo import analysis_collection

def process_analysis_job(job_id: str):
    # marking job as processing
    analysis_collection.update_one(
        {"job_id": job_id},
        {"$set": {"status": "processing"}}
    )

    #long-running task(ai later)
    time.sleep(5)

    #mock analysis result shown
    result = {
        "intent": "payment_followup",
        "urgency": "high",
        "summary": "Request to clear pending invoice"
    }

    #mark job as completed
    analysis_collection.update_one(
        {"job_id": job_id},
        {
            "$set": {
                "status": "completed",
                "result": result
            }
        }
    )