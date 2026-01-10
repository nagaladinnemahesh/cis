import time
from app.db.mongo import analysis_collection
from app.services.gemini import analyze_content_with_gemini, generate_reply_with_gemini

def process_analysis_job(job_id: str):
    # fetch job
    job = analysis_collection.find_one({"job_id": job_id})


    if not job:
        return

    try:
        # route based on contetn type
        if job["content_type"] == "email_reply":
            result = generate_reply_with_gemini(job["content"])
        else:
            result = analyze_content_with_gemini(
                job["content_type"], job["content"]
            )


    # marking job as completed
        analysis_collection.update_one(
            {"job_id": job_id},
            {"$set": {"status": "completed", "result": result}}
        )

    # #long-running task(ai later)
    # time.sleep(5)

    # try:
    #     result = analyze_content_with_gemini(
    #         content_type=job["content_type"],
    #         content=job["content"]
    #     )

    # #mock analysis result shown
    # result = {
    #     "intent": "payment_followup",
    #     "urgency": "high",
    #     "summary": "Request to clear pending invoice"
    # }

    #mark job as completed
        # analysis_collection.update_one(
        #     {"job_id": job_id},
        #     {
        #         "$set": {
        #             "status": "completed",
        #             "result": result
        #         }
        #     }
        # )
    
    except Exception as e:
        analysis_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "failed",
                    "error": str(e)
                }
            }
        )