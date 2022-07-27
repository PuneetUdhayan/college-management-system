from fastapi import FastAPI

from app.routers import student, teacher


app = FastAPI(
    title = 'College Managment System API',
    description='API to manage teacher, students and classes of a college.',
    version='0.0.1'
)

app.include_router(student.router)
app.include_router(teacher.router)