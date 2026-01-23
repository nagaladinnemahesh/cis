from app.db.mongo import analysis_collection

def retrive_context(content_type: str, limit: int = 3):
    """
    Lightweight RAG:
    Retrive recent completed analyses for the same content content_type
    """

    cursor = analysis_collection.find(
        {
            "content_type": content_type,
            "status": "completed",
            "result": {"$ne": None}
        },
        {
            "_id": 0,
            "result": 1
        }
    ).sort("created_at", -1).limit(limit)

    contexts = []
    for doc in cursor:
        contexts.append(doc["result"])

    return contexts