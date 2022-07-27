import json

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_teacher(set_up_env):
    response = client.get("/teacher/")
    assert response.json() == [
        {'id': 1, 'name': 'Teacher 1', 'email': 'teacher1@gmail.com'}]


def test_get_teacher_exception(set_up_env):
    response = client.get("/teacher/", params={"teacher_id": 1000})
    assert response.json() == []
