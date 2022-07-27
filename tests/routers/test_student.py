import json

from fastapi.testclient import TestClient
from pytest import param

from app.main import app


client = TestClient(app)


def test_get_students(set_up_env):
    response = client.get("/student/")
    assert response.json() == [
        {'id': 1, 'name': 'puneet', 'email': 'puneetudhayan@gmail.com'}]


def test_insert_student(set_up_env):
    new_student = {
        "name": "Student 2",
        "email": "student2@email.com"
    }
    response = client.post("/student/", data=json.dumps(new_student))
    assert response.json() == {
        "id": 2,
        "name": "Student 2",
        "email": "student2@email.com"
    }


def test_update_student_info(set_up_env):
    update_student = {
        "id": 2,
        "name": "Student 2 Updated",
        "email": "student2@email.com"
    }
    response = client.put("/student/", data=json.dumps(update_student))
    assert response.json() == {
        "id": 2,
        "name": "Student 2 Updated",
        "email": "student2@email.com"
    }
    response = client.get("/student/", params={"student_id": 2})
    assert response.json() == [{
        "id": 2,
        "name": "Student 2 Updated",
        "email": "student2@email.com"
    }]


def test_add_course(set_up_env):
    response = client.put("/student/add-course",
                          params={"course_id": 1, "student_id": 2})
    assert response.json() == {
        "course_id": "1",
        "id": 2,
        "student_id": "2"
    }


def test_remove_course(set_up_env):
    response = client.put("/student/remove-course",
                          params={"course_id": 1, "student_id": 2})
    assert response.json() == {
        "student_id": "2",
        "course_id": "1",
        "id": 2
    }


def test_get_days_classes(set_up_env):
    reponse = client.get("/student/classes", params={"student_id" : 1, "day" : "MONDAY"})
    assert reponse.json() == [{
        "start_time" : "6:30",
        "end_time" : "8:10",
        "course" : "Course 1"
    }]


def test_remove_student(set_up_env):
    client.delete("/student/", params={"student_id": 2})
    response = client.get("/student/", params={"student_id": 2})
    assert response.json() == []
