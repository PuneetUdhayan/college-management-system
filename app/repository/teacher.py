from typing import List

from sqlalchemy.orm import Session

from app.database.models import Teacher as TeacherDatabaseModel
from app.schemas import CreateTeacher as CreateTeacherSchema
from app.schemas import Teacher as TeacherSchema
from app.repository.custom_exceptions import TeacherNotFound


def get_teachers(db: Session, teacher_id: int = None) -> List:
    """Retreive teacher from database. If teacher_id is provided teacher
    with given ID will be retrieved

    Args:
        db (Session): Database session
        teacher_id (int, optional): Teacher ID. Defaults to None.

    Returns:
        List: _description_
    """
    if teacher_id:
        teachers = db.query(TeacherDatabaseModel).\
            filter(TeacherDatabaseModel.id == teacher_id).\
            all()
    else:
        teachers = db.query(TeacherDatabaseModel).all()
    return teachers


def insert_teacher(teacher_data: CreateTeacherSchema, db: Session) -> TeacherDatabaseModel:
    """Insert new teacher into database

    Args:
        teacher_data (TeacherSchema): Teacher pydantic class
        db (Session): database session

    Returns:
        TeacherDatabaseModel: Teacher database model
    """
    teacher_database_model = TeacherDatabaseModel(
        name=teacher_data.name,
        email=teacher_data.email
    )
    db.add(teacher_database_model)
    db.commit()
    db.refresh(teacher_database_model)
    return teacher_database_model


def update_teacher_info(teacher_data: TeacherSchema, db: Session) -> TeacherDatabaseModel:
    """Update name and email of a teacher

    Args:
        teacher_data (TeacherSchema): Teacher pydantic class
        db (Session): Database session

    Raises:
        Exception: When no teacher is found for the given ID

    Returns:
        TeacherDatabaseModel: teacher database model
    """
    teacher_database_model = db.query(TeacherDatabaseModel).\
        filter(TeacherDatabaseModel.id == teacher_data.id).\
        first()
    if not teacher_database_model:
        raise TeacherNotFound()
    teacher_database_model.name = teacher_data.name
    teacher_database_model.email = teacher_data.email
    db.commit()
    return teacher_database_model


def remove_teacher(teacher_id: int, db: Session) -> TeacherDatabaseModel:
    """Delete teacher from database

    Args:
        teacher_id (int): Id of the teacher that needs to be deleted
        db (Session): Database session

    Raises:
        Exception: Raises exception when no teacher if found for the given ID.

    Returns:
        TeacherDatabaseModel: teacher database model
    """
    teacher_database_model = db.query(TeacherDatabaseModel).\
        filter(TeacherDatabaseModel.id == teacher_id).\
        first()
    if not teacher_database_model:
        raise TeacherNotFound()
    db.delete(teacher_database_model)
    db.commit()
    return teacher_database_model