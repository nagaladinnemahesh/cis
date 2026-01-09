from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routers.analyze import router as analyze_router

app = FastAPI(
    title = 'CIS - Content Intelligence Service',
    version = "1.0.0"
)

app.include_router(analyze_router)

@app.get('/health')
def health_check():
    return{"status": 'ok'}