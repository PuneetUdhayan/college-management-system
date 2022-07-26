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
