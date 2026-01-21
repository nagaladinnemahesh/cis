from app.db.mongo import analysis_collection
from app.services.gemini import analyze_content_with_gemini, generate_reply_with_gemini

def process_analysis_job(job_id: str):
    # print("CIS worker started for:", job_id)

    job = analysis_collection.find_one({"job_id": job_id})

    if not job:
        # print("Job not found in DB:", job_id)
        analysis_collection.update_one(
            {"job_id": job_id},
            {"$set": {"status": "failed", "error": "Job not found"}}
        )
        return

    try:
        # print("Processing content for:", job_id)

        if job["content_type"] == "email_reply":
            result = generate_reply_with_gemini(job["content"])
        else:
            result = analyze_content_with_gemini(
                job["content_type"],
                job["content"]
            )

        analysis_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "completed",
                    "result": result
                }
            }
        )

        print("CIS job completed:", job_id)

    except Exception as e:
        # print("CIS job failed:", job_id, str(e))

        analysis_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "failed",
                    "error": str(e)
                }
            }
        )
