import pytest

from app.repository.time_conversion import TimeConversions, IncorrectTimeFormat, IncorrectMinutesValue


def test_minutes_to_time():
    assert TimeConversions().minutes_to_time(390) == "6:30"
    with pytest.raises(IncorrectMinutesValue):
        TimeConversions().minutes_to_time(-90)
    with pytest.raises(IncorrectMinutesValue):
        TimeConversions().minutes_to_time(2000)


def test_time_to_minutes():
    assert TimeConversions().time_to_minutes("6:30") == 390
    with pytest.raises(IncorrectTimeFormat):
        TimeConversions().time_to_minutes("630")
    with pytest.raises(IncorrectTimeFormat):
        TimeConversions().time_to_minutes("36:30")
    with pytest.raises(IncorrectTimeFormat):
        TimeConversions().time_to_minutes("12:70")
