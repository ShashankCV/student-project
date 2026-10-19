import os

from fastapi import APIRouter, Depends, HTTPException
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student


router = APIRouter(prefix="/ai", tags=["AI Query"])


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@router.post("/query-students")
def ask_student_database(payload: QueryRequest, database: Session = Depends(get_db)):
    students = database.scalars(select(Student).order_by(Student.id)).all()
    context_data = "\n".join(
        f"ID: {student.id}, Name: {student.name}, Age: {student.age}, Course: {student.course}"
        for student in students
    ) or "No student records are currently in the database."

    prompt = f"""You are a helpful assistant. Answer the user's question using only the student records below. If the records do not contain the answer, say so.

Student records:
{context_data}

User question: {payload.question}
Answer:"""

    try:
        model = ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.2:1b"), temperature=0)
        response = model.invoke(prompt)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="The local Ollama model is unavailable. Start Ollama and ensure the configured model is installed.",
        ) from error

    answer = response.content if hasattr(response, "content") else str(response)
    return {"question": payload.question, "answer": answer}