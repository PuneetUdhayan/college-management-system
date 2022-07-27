from fastapi import FastAPI

from app.routers import student, teacher, courses

## DB Set up 
from app.database import database
from app.database import models

models.Base.metadata.create_all(database.engine)

db = database.get_db().__next__()
days = db.query(models.DayOfWeek).all()

if not days:
    db.add(models.DayOfWeek(id=1, name='MONDAY'))
    db.add(models.DayOfWeek(id=2, name='TUESDAY'))
    db.add(models.DayOfWeek(id=3, name='WEDNESDAY'))
    db.add(models.DayOfWeek(id=4, name='THURSDAY'))
    db.add(models.DayOfWeek(id=5, name='FRIDAY'))
    db.add(models.DayOfWeek(id=6, name='SATURDAY'))
    db.add(models.DayOfWeek(id=7, name='SUNDAY'))

db.commit()
# End of db setup

app = FastAPI(
    title = 'College Managment System API',
    description='API to manage teacher, students and classes of a college.',
    version='0.0.1'
)

app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(courses.router)