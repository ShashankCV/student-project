from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.schemas import StudentRead


router = APIRouter(prefix="/students", tags=["Students"])


@router.get("", response_model=list[StudentRead])
def list_students(database: Session = Depends(get_db)):
    return database.scalars(select(Student).order_by(Student.id)).all()


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, database: Session = Depends(get_db)):
    student = database.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student