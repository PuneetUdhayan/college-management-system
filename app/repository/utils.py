from sqlalchemy.orm import Session

from app.database.models import DayOfWeek as DayOfWeekDatabaseModel
from app.repository.custom_exceptions import IncorrectDayOfWeek


def get_day_id(day:str, db:Session) -> id:
    """Get ID for the given day of week

    Args:
        day (str): Day of the week
        db (Session): Database session

    Raises:
        IncorrectDayOfWeek: Raises exception when no entry if found for the given day

    Returns:
        int: Day ID
    """
    day_of_week = db.query(DayOfWeekDatabaseModel).filter(DayOfWeekDatabaseModel.name == day).first()
    if not day_of_week:
        raise IncorrectDayOfWeek()
    return day_of_week.id