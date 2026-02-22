
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from routes.documents import router as document_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from routes.documents import router as document_router


app = FastAPI(
    title="StudyMate AI",
    description="RAG-powered study assistant using Claude",
    version="1.0.0"
)

# Allow frontend (React/Next.js) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router, prefix="/documents", tags=["Documents"])


@app.get("/")
async def home():
    return {"message": "StudyMate AI is running!", "status": "ok"}