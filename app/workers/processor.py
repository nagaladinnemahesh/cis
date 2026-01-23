from app.db.mongo import analysis_collection
from app.services.gemini import (
    analyze_content_with_gemini,
    generate_reply_with_gemini,
)
from app.services.rag import retrive_context


def process_analysis_job(job_id: str):
    job = analysis_collection.find_one({"job_id": job_id})
    print("processing job:", job_id)

    if not job:
        print("job not found")
        return

    try:
       
        # Retrieve contextual memory (Lightweight RAG)
        contexts = retrive_context(job["content_type"])
        # print(f" Retrived {len(contexts)} RAG context items for job {job_id}")
        for i, ctx in enumerate(contexts, start = 1):
            print(f" RAG[{i}] → intent={ctx.get('intent')}, urgency={ctx.get('urgency')}")

        
        # Route based on content type
        if job["content_type"] == "email_reply":
            result = generate_reply_with_gemini(
                job["content"],
                contexts=contexts,
            )
        else:
            result = analyze_content_with_gemini(
                content_type=job["content_type"],
                content=job["content"],
                contexts=contexts,  # RAG injection
            )

        #Mark job as completed
        analysis_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "completed",
                    "result": result,
                }
            },
        )

    except Exception as e:
        error_msg = str(e)
        print("🔥 CIS job failed:", job_id, error_msg)

        # Graceful fallback (CRITICAL)
        analysis_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "completed",
                    "result": {
                        "intent": "unknown",
                        "urgency": "low",
                        "summary": "AI analysis temporarily unavailable.",
                        "suggested_action": "Review the email manually.",
                    },
                    "error": error_msg,
                }
            },
        )
