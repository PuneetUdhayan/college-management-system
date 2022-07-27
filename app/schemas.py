from typing import List

from pydantic import BaseModel


class CreateStudent(BaseModel):

    name: str
    email: str


class Student(BaseModel):

    id: int
    name: str
    email: str

    class Config():
        orm_mode = True


class CreateTeacher(BaseModel):

    name: str
    email: str


class Teacher(BaseModel):

    id: int
    name: str
    email: str

    class Config():
        orm_mode = True


class CreateClass(BaseModel):

    day_of_week: str
    start_time: str
    end_time: str


class CreateCourse(BaseModel):

    name: str
    teacher_id: int
    classes: List[CreateClass]


class Course(BaseModel):

    id: int
    name: str
    teacher_id: int

    class Config():
        orm_mode = True


class CourseInfo(BaseModel):

    id: int
    name: str
    teacher: str
