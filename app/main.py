from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from app.routers import student


app = FastAPI(
    title = 'College Managment System API',
    description='API to manage teacher, students and classes of a college.',
    version='0.0.1'
)

app.include_router(student.router)