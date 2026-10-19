from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.schemas import StudentRead, StudentUpdate


router = APIRouter(prefix="/students", tags=["Students"])


@router.put("/{student_id}", response_model=StudentRead)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    database: Session = Depends(get_db),
):
    student = database.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, field, value)

    database.commit()
    database.refresh(student)
    return student