from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Student(Base):
    __tablename__ = 'STUDENT'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)


class Teacher(Base):
    __tablename__ = 'TEACHER'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)


class Course(Base):
    __tablename__ = 'COURSE'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('TEACHER.id'), nullable=False)


class Classes(Base):
    __tablename__ = 'CLASSES'

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer, ForeignKey('DAY_OF_WEEK.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('DAY_OF_WEEK.id'), nullable=False)
    start_time = Column(Integer)
    end_time = Column(Integer)


class DayOfWeek(Base):
    __tablename__ = 'DAY_OF_WEEK'

    id = Column(Integer, primary_key=True, index=False)
    name = Column(String)


class StudentCourseMap(Base):
    __tablename__ = 'STUDENT_COURSE_MAP'

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String, ForeignKey('COURSE.id'), nullable=False)
    student_id = Column(String, ForeignKey('STUDENT.id'), nullable=False)
