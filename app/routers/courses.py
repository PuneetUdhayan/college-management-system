from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repository import courses
from app.schemas import CourseInfo, CreateClass, CreateCourse, Course, CourseInfo
from app.repository.custom_exceptions import CourseNotFound, ClassNotFound


router = APIRouter(
    prefix="/course",
    tags=['Course']
)


@router.get('/', response_model=List[CourseInfo])
def get_courses(course_id: Optional[int] = None, db: Session = Depends(get_db)):
    return courses.get_courses(db=db, course_id=course_id)


@router.post('/', response_model=Course)
def insert_course(course_data: CreateCourse, db: Session = Depends(get_db)):
    return courses.insert_course(course_data=course_data, db=db)


@router.put('/', response_model=Course)
def update_course_info(course_data: Course, db: Session = Depends(get_db)):
    try:
        return courses.update_course_info(course_data=course_data, db=db)
    except CourseNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))


@router.delete('/', response_model=Course)
def remove_course(course_id: int, db: Session = Depends(get_db)):
    try:
        return courses.remove_course(course_id=course_id, db=db)
    except CourseNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))


@router.get('/class')
def get_classes_for_course(course_id: int, db: Session = Depends(get_db)):
    return courses.get_classes_for_course(db=db, course_id=course_id)


@router.post('/class')
def insert_class_for_course(course_id:int, class_data: CreateClass, db: Session = Depends(get_db)):
    return courses.insert_class_for_course(course_id=course_id, class_data=class_data, db=db)


@router.delete('/class')
def remove_class_for_course(class_id: int, db: Session = Depends(get_db)):
    try:
        return courses.remove_class_for_course(class_id=class_id, db=db)
    except ClassNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
