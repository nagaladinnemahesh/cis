from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routers.analyze import router as analyze_router
from app.routers.result import router as result_router
from app.routers.reply import router as reply_router

app = FastAPI(
    title = 'CIS - Content Intelligence Service',
    version = "1.0.0"
)

app.include_router(analyze_router)
app.include_router(result_router)
app.include_router(reply_router)

@app.get('/health')
def health_check():
    return{"status": 'ok'}