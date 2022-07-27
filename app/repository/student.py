from typing import List

from sqlalchemy.orm import Session

from app.database.models import Student as StudentDatabaseModel
from app.database.models import StudentCourseMap as StudentCourseMapDatabaseModel
from app.database.models import Classes as ClassesDatabaseModel
from app.schemas import CreateStudent as CreateStudentSchema
from app.schemas import Student as StudentSchema
from app.repository.custom_exceptions import StudentNotFound, CourseNotFound, IncorrectDayOfWeek
from app.repository.utils import get_day_id


def get_students(db: Session, student_id: int = None) -> List:
    """Retreive student from database. If student_id is provided student
    with given ID will be retrieved

    Args:
        db (Session): Database session
        student_id (int, optional): Student ID. Defaults to None.

    Returns:
        List: _description_
    """
    if student_id:
        students = db.query(StudentDatabaseModel).\
            filter(StudentDatabaseModel.id == student_id).\
            all()
    else:
        students = db.query(StudentDatabaseModel).all()
    return students


def insert_student(student_data: CreateStudentSchema, db: Session) -> StudentDatabaseModel:
    """Insert new student into database

    Args:
        student_data (StudentSchema): Student pydantic class
        db (Session): database session

    Returns:
        StudentDatabaseModel: Student database model
    """
    student_database_model = StudentDatabaseModel(
        name=student_data.name,
        email=student_data.email
    )
    db.add(student_database_model)
    db.commit()
    db.refresh(student_database_model)
    return student_database_model


def update_student_info(student_data: StudentSchema, db: Session) -> StudentDatabaseModel:
    """Update name and email of a student

    Args:
        student_data (StudentSchema): Student pydantic class
        db (Session): Database session

    Raises:
        Exception: When no student is found for the given ID

    Returns:
        StudentDatabaseModel: student database model
    """
    student_database_model = db.query(StudentDatabaseModel).\
        filter(StudentDatabaseModel.id == student_data.id).\
        first()
    if not student_database_model:
        raise StudentNotFound()
    student_database_model.name = student_data.name
    student_database_model.email = student_data.email
    db.commit()
    return student_database_model


def remove_student(student_id: int, db: Session) -> StudentDatabaseModel:
    """Delete student from database

    Args:
        student_id (int): Id of the student that needs to be deleted
        db (Session): Database session

    Raises:
        Exception: Raises exception when no student if found for the given ID.

    Returns:
        StudentDatabaseModel: student database model
    """
    student_database_model = db.query(StudentDatabaseModel).\
        filter(StudentDatabaseModel.id == student_id).\
        first()
    if not student_database_model:
        raise StudentNotFound()
    db.delete(student_database_model)
    db.commit()
    return student_database_model


def add_course(course_id: int, student_id: int,db: Session):
    """Add course for a student

    Args:
        course_id (int): Id of the course
        student_id (int): Id of the student
        db (Session): DB session

    Returns:
        StudentCourseDatabaseModel: Student course mapping
    """
    student_course = StudentCourseMapDatabaseModel(
        course_id = course_id,
        student_id = student_id
    )
    db.add(student_course)
    db.commit()
    db.refresh(student_course)
    return student_course


def remove_course(course_id: int, student_id: int, db: Session):
    """Remove course for a student

    Args:
        course_id (int): Course ID
        student_id (int): Student ID
        db (Session): Database session

    Raises:
        CourseNotFound: Exception raised of student course mapping does not exist

    Returns:
        StudentCourseDatabaseModel: Student course mapping
    """
    student_course = db.query(StudentCourseMapDatabaseModel).\
        filter(
            StudentCourseMapDatabaseModel.course_id == course_id, 
            StudentCourseMapDatabaseModel.student_id == student_id
        ).first()
    if not student_course:
        raise CourseNotFound()
    db.delete(student_course)
    db.commit()
    return student_course


def get_days_classes(student_id: int, day:str, db:Session):
    """Returns all the classes a student has for the given day

    Args:
        student_id (int): Student ID
        day (str): Day of week in the format MONDAY, TUESDAY ... 
        db (Session): Database Session
    """
    day_id = get_day_id(day=day, db=db)
    classes = db.query(ClassesDatabaseModel).\
                select_from(StudentCourseMapDatabaseModel).\
                join(
                    ClassesDatabaseModel, 
                    StudentCourseMapDatabaseModel.course_id==ClassesDatabaseModel.course_id
                ).\
                filter(
                    StudentCourseMapDatabaseModel.student_id==student_id,
                    ClassesDatabaseModel.day_of_week == day_id
                ).order_by(ClassesDatabaseModel.start_time).all()
    return classes
    
