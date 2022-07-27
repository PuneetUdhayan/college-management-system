from calendar import c
from typing import List

from sqlalchemy.orm import Session

from app.database.models import Course as CourseDatabaseModel
from app.database.models import Teacher as TeacherDatabaseModel
from app.database.models import Classes as ClassesDatabaseModel
from app.database.models import DayOfWeek as DayOfWeekDatabaseModel
from app.schemas import CreateCourse as CreateCourseSchema
from app.schemas import Course as CourseSchema
from app.schemas import CreateClass as CreateClassSchema
from app.schemas import CourseInfo as CourseInfoSchema
from app.repository.custom_exceptions import CourseNotFound
from app.repository.utils import get_day_id
from app.repository.time_conversion import TimeConversions


def format_course_output(course_teacher_info: List) -> List[CourseInfoSchema]:
    info = []
    for course, teacher in course_teacher_info:
        info.append(CourseInfoSchema(
            id=course.id,
            name=course.name,
            teacher=teacher.name
        ))
    return info


def get_courses(db: Session, course_id: int = None) -> List:
    """Retreive course from database. If course_id is provided course
    with given ID will be retrieved

    Args:
        db (Session): Database session
        course_id (int, optional): Course ID. Defaults to None.

    Returns:
        List: _description_
    """
    if course_id:
        courses = db.query(CourseDatabaseModel, TeacherDatabaseModel).\
            join(TeacherDatabaseModel).\
            filter(CourseDatabaseModel.id == course_id).\
            all()
    else:
        courses = db.query(CourseDatabaseModel, TeacherDatabaseModel).\
            join(TeacherDatabaseModel).all()
    return format_course_output(courses)


def insert_course(course_data: CreateCourseSchema, db: Session) -> CourseDatabaseModel:
    """Insert new course into database

    Args:
        course_data (CourseSchema): Course pydantic class
        db (Session): database session

    Returns:
        CourseDatabaseModel: Course database model
    """
    course_database_model = CourseDatabaseModel(
        name=course_data.name,
        teacher_id=course_data.teacher_id
    )
    db.add(course_database_model)
    db.commit()
    db.refresh(course_database_model)
    for cl in course_data.classes:
        insert_class_for_course(course_id = course_database_model.id, class_data=cl, db=db)
    return course_database_model


def update_course_info(course_data: CourseSchema, db: Session) -> CourseDatabaseModel:
    """Update name and email of a course

    Args:
        course_data (CourseSchema): Course pydantic class
        db (Session): Database session

    Raises:
        Exception: When no course is found for the given ID

    Returns:
        CourseDatabaseModel: course database model
    """
    course_database_model = db.query(CourseDatabaseModel).\
        filter(CourseDatabaseModel.id == course_data.id).\
        first()
    if not course_database_model:
        raise CourseNotFound()
    course_database_model.name = course_data.name
    course_database_model.teacher_id = course_data.teacher_id
    db.commit()
    return course_database_model


def remove_course(course_id: int, db: Session) -> CourseDatabaseModel:
    """Delete course from database

    Args:
        course_id (int): Id of the course that needs to be deleted
        db (Session): Database session

    Raises:
        Exception: Raises exception when no course if found for the given ID.

    Returns:
        CourseDatabaseModel: course database model
    """
    course_database_model = db.query(CourseDatabaseModel).\
        filter(CourseDatabaseModel.id == course_id).\
        first()
    if not course_database_model:
        raise CourseNotFound()
    db.delete(course_database_model)
    db.commit()
    return course_database_model


def get_classes_for_course(course_id: int, db: Session):
    classes =  db.query(ClassesDatabaseModel, DayOfWeekDatabaseModel).\
        join(DayOfWeekDatabaseModel, ClassesDatabaseModel.day_of_week == DayOfWeekDatabaseModel.id).\
        filter(ClassesDatabaseModel.course_id == course_id).\
        all()
    class_data = []
    for cl, day in classes:
        class_data.append({
            'id' : cl.id,
            'day_of_week' : day.name,
            'course_id' : cl.course_id,
            'start_time' : TimeConversions.minutes_to_time(cl.start_time),
            'end_time' : TimeConversions.minutes_to_time(cl.end_time)
        })
    return class_data


def insert_class_for_course(course_id: int, class_data: CreateClassSchema, db: Session):
    day_of_week_id = get_day_id(day=class_data.day_of_week, db=db)
    start_time = TimeConversions.time_to_minutes(class_data.start_time)
    end_time = TimeConversions.time_to_minutes(class_data.end_time)
    class_database_model = ClassesDatabaseModel(
        course_id = course_id,
        day_of_week = day_of_week_id,
        start_time = start_time,
        end_time = end_time
    )
    db.add(class_database_model)
    db.commit()
    db.refresh(class_database_model)
    return {
        "id" : class_database_model.id,
        "day_of_week" : class_data.day_of_week,
        "course_id" : class_database_model.course_id,
        "start_time" : TimeConversions.minutes_to_time(class_database_model.start_time),
        "end_time" : TimeConversions.minutes_to_time(class_database_model.end_time)
    }


def remove_class_for_course(class_id: int, db: Session):
    class_database_model = db.query(ClassesDatabaseModel).\
        filter(ClassesDatabaseModel.id == class_id).first()
    db.delete(class_database_model)
    db.commit()
    return {
        "id" : class_database_model.id,
        "day_of_week" : class_database_model.id,
        "course_id" : class_database_model.course_id,
        "start_time" : TimeConversions.minutes_to_time(class_database_model.start_time),
        "end_time" : TimeConversions.minutes_to_time(class_database_model.end_time)
    }
