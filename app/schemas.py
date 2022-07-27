from pydantic import BaseModel


class CreateStudent(BaseModel):

    name: str
    email: str

    class Config():
        orm_mode = True


class Student(BaseModel):

    id: int
    name: str
    email: str

    class Config():
        orm_mode = True
