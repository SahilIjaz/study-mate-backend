from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Use absolute import style when running from project root
from controllers.document_controller import upload_pdf, ask_question

router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported."})
    result = await upload_pdf(file)
    return result


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask(body: QuestionRequest):
    if not body.question.strip():
        return JSONResponse(status_code=400, content={"error": "Question cannot be empty."})
    result = await ask_question(body.question)
    return result