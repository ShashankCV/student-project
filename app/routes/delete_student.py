from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student


router = APIRouter(prefix="/students", tags=["Students"])


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, database: Session = Depends(get_db)):
    student = database.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    database.delete(student)
    database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)