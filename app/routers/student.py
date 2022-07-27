from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repository import student
from app.schemas import CreateStudent, Student
from app.repository.custom_exceptions import CourseNotFound, StudentNotFound


router = APIRouter(
    prefix="/student",
    tags=['Student']
)


@router.get('/', response_model=List[Student])
def get_students(student_id: Optional[int] = None, db: Session = Depends(get_db)):
    return student.get_students(db=db, student_id=student_id)


@router.post('/', response_model=Student)
def insert_student(student_data : CreateStudent, db: Session = Depends(get_db)):
    return student.insert_student(student_data=student_data, db=db)


@router.put('/', response_model=Student)
def update_student_info(student_data : Student, db: Session = Depends(get_db)):
    try:
        return student.update_student_info(student_data=student_data, db=db)
    except StudentNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))


@router.delete('/', response_model=Student)
def remove_student(student_id: int, db: Session = Depends(get_db)):
    try:
        return student.remove_student(student_id=student_id, db=db)
    except StudentNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))


@router.put('/add-course')
def add_course(course_id: int, student_id: int,db: Session = Depends(get_db)):
    return student.add_course(course_id=course_id, student_id=student_id, db=db)


@router.put('/remove-course')
def remove_course(course_id: int, student_id: int, db: Session = Depends(get_db)):
    try:
        return student.remove_course(course_id=course_id, student_id=student_id, db=db)
    except CourseNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))


@router.get('/classes')
def get_days_classes(student_id:int, day: Optional[str] = None, db: Session = Depends(get_db)):
    if not day:
        day = datetime.today().strftime('%A').upper()
    return student.get_days_classes(student_id=student_id, day=day, db=db)
