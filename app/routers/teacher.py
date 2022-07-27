from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repository import teacher
from app.schemas import CreateTeacher, Teacher
from app.repository.custom_exceptions import TeacherNotFound


router = APIRouter(
    prefix="/teacher",
    tags=['Teacher']
)


@router.get('/', response_model=List[Teacher])
def get_teachers(teacher_id: Optional[int] = None, db: Session = Depends(get_db)):
    return teacher.get_teachers(db=db, teacher_id=teacher_id)


@router.post('/', response_model=Teacher)
def insert_teacher(teacher_data : CreateTeacher, db: Session = Depends(get_db)):
    return teacher.insert_teacher(teacher_data=teacher_data, db=db)


@router.put('/', response_model=Teacher)
def update_teacher_info(teacher_data : Teacher, db: Session = Depends(get_db)):
    try:
        return teacher.update_teacher_info(teacher_data=teacher_data, db=db)
    except TeacherNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))


@router.delete('/', response_model=Teacher)
def remove_teacher(teacher_id: int, db: Session = Depends(get_db)):
    try:
        return teacher.remove_teacher(teacher_id=teacher_id, db=db)
    except TeacherNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))