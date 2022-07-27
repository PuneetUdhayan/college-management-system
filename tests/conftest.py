"""  
Module contains fixture that creates a SQL list database for testing
"""
import os

import pytest

from app.database import database
from app.database import models


@pytest.fixture(scope="session")
def set_up_env():

    # Set connection string in SQL lite DB
    os.environ['SQLALCHAMY_DATABASE_URL'] = 'sqlite:///./college.db'

    # Delete existing database
    if 'college.db' in os.listdir('.'):
        os.remove('college.db')

    # Create tables
    models.Base.metadata.create_all(database.engine)

    # Insert data for testing
    db = database.get_db().__next__()

    db.add(models.DayOfWeek(id=1, name='MONDAY'))
    db.add(models.DayOfWeek(id=2, name='TUESDAY'))
    db.add(models.DayOfWeek(id=3, name='WEDNESDAY'))
    db.add(models.DayOfWeek(id=4, name='THURSDAY'))
    db.add(models.DayOfWeek(id=5, name='FRIDAY'))
    db.add(models.DayOfWeek(id=6, name='SATURDAY'))
    db.add(models.DayOfWeek(id=7, name='SUNDAY'))

    db.add(models.Student(name="puneet", email = "puneetudhayan@gmail.com"))
    db.add(models.Teacher(name="Teacher 1", email="teacher1@gmail.com"))
    db.add(models.Course(name="Course 1", teacher_id = 1))
    db.add(models.Classes(day_of_week=1, course_id = 1, start_time = 390, end_time=490))

    db.commit()
