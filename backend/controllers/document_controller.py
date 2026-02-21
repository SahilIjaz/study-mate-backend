import os
import anthropic
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

from utils.pdf_parser import extract_text
from utils.chunker import chunk_text
from utils.embeddings import get_embeddings, get_single_embedding
from utils.vector_store import add_chunks, query_chunks

api_key = os.getenv("ANTHROPIC_API_KEY")
claude = anthropic.Anthropic(api_key=api_key)


async def upload_pdf(file: UploadFile) -> dict:
    file_path = f"backend/uploads/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    raw_text = extract_text(file_path)
    if not raw_text:
        return {"error": "Could not extract text from PDF."}

    chunks = chunk_text(raw_text)
    embeddings = get_embeddings(chunks)

    chunk_objects = [
        {
            "text": chunks[i],
            "source_file": file.filename,
            "embedding": embeddings[i]
        }
        for i in range(len(chunks))
    ]
    add_chunks(chunk_objects)

    return {
        "message": "PDF uploaded and indexed successfully!",
        "filename": file.filename,
        "chunks_stored": len(chunks)
    }


async def ask_question(question: str) -> dict:
    query_embedding = get_single_embedding(question)
    relevant_chunks = query_chunks(query_embedding, top_k=5)

    if not relevant_chunks:
        return {"answer": "No documents uploaded yet. Please upload a PDF first.", "sources": []}

    context = "\n\n---\n\n".join([
        f"[Source: {c['source_file']}]\n{c['text']}"
        for c in relevant_chunks
    ])

    message = claude.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a helpful study assistant. Answer the question below using ONLY the provided context from uploaded documents. If the answer is not in the context, say so clearly.

<context>
{context}
</context>

<question>
{question}
</question>

Provide a clear, well-structured answer. Mention which source file the information came from."""
            }
        ]
    )

    answer = message.content[0].text
    sources = list(set(c["source_file"] for c in relevant_chunks))

    return {
        "answer": answer,
        "sources": sources
    }