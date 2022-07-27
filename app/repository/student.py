from typing import List

from sqlalchemy.orm import Session

from app.database.models import Student as StudentDatabaseModel
from app.schemas import CreateStudent as CreateStudentSchema
from app.schemas import Student as StudentSchema
from app.repository.custom_exceptions import StudentNotFound


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


def insert_student(student_data: StudentSchema, db: Session) -> StudentDatabaseModel:
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
        all()
    if not student_database_model:
        raise StudentNotFound()
    db.delete(student_database_model)
    db.commit()
    return student_database_model
