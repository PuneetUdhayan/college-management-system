import json

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_student(set_up_env):
    response = client.get("/student/")
    assert response.json() == [
        {'id': 1, 'name': 'puneet', 'email': 'puneetudhayan@gmail.com'}]
