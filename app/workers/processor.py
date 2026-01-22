from app.db.mongo import analysis_collection
from app.services.gemini import analyze_content_with_gemini, generate_reply_with_gemini
from app.services.rag import retrive_context

def process_analysis_job(job_id: str):
    job = analysis_collection.find_one({"job_id": job_id})
    print("processing job:", job_id)

    if not job:
        return

    try:
        if job["content_type"] == "email_reply":
            result = generate_reply_with_gemini(job["content"])
        else:
            result = analyze_content_with_gemini(
                job["content_type"], job["content"]
            )

        # ✅ mark completed
        analysis_collection.update_one(
            {"job_id": job_id},
            {"$set": {"status": "completed", "result": result}}
        )

    except Exception as e:
        error_msg = str(e)
        print("🔥 CIS job failed:", job_id, error_msg)

        # ✅ graceful fallback (VERY IMPORTANT)
        analysis_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "completed",
                    "result": {
                        "intent": "unknown",
                        "urgency": "low",
                        "summary": "AI analysis temporarily unavailable.",
                        "suggested_action": "Review the email manually."
                    },
                    "error": error_msg
                }
            }
        )
