import json

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_course(set_up_env):
    response = client.get("/course/")
    assert response.json() == [
        {'id': 1, 'name': 'Course 1', 'teacher': 'Teacher 1'}]


def test_insert_course(set_up_env):
    new_course = {
        "name": "Test 2",
        "teacher_id": 1,
        "classes": [
            {
                "day_of_week": "MONDAY",
                "start_time": "9:30",
                "end_time": "10:30"
            },
            {
                "day_of_week": "TUESDAY",
                "start_time": "11:30",
                "end_time": "12:30"
            }
        ]
    }
    response = client.post("/course/", data=json.dumps(new_course))
    created_course = response.json()
    assert isinstance(created_course['id'], int)
    assert created_course['name'] == 'Test 2'
    assert created_course['teacher_id'] == 1
    response = client.get("/course/")
    assert len(response.json()) == 2


def test_update_course(set_up_env):
    update_course = {
        "id": 2,
        "name": "Updated course",
        "teacher_id": 1
    }
    response = client.put('/course/', data=json.dumps(update_course))
    updated_course = response.json()
    assert updated_course['id'] == 2
    assert updated_course['name'] == 'Updated course'
    assert updated_course['teacher_id'] == 1
    response = client.get(
        '/course/', params={"course_id": 2}, data=json.dumps(update_course))
    updated_course = response.json()[0]
    assert updated_course['id'] == 2
    assert updated_course['name'] == 'Updated course'
    assert updated_course['teacher'] == 'Teacher 1'


def test_get_classes_for_course():
    response = client.get("/course/class", params={"course_id": 2})
    response = response.json()
    assert response[0] == {
        "id": 2,
        "course_id" : 2,
        "day_of_week": "MONDAY",
        "start_time": "9:30",
        "end_time": "10:30"
    }
    assert response[1] == {
        "id": 3,
        "course_id" : 2,
        "day_of_week": "TUESDAY",
        "start_time": "11:30",
        "end_time": "12:30"
    }


def test_insert_class_for_course():
    new_class = {
        "day_of_week": "WEDNESDAY",
        "start_time": "9:30",
        "end_time": "10:30"
    }
    response = client.post("/course/class",params={"course_id":2}, data=json.dumps(new_class))
    assert response.json() == {
        "id": 4,
        "course_id" : 2,
        "day_of_week": "WEDNESDAY",
        "start_time": "9:30",
        "end_time": "10:30"
    }


def test_remove_class_for_course():
    response = client.delete("/course/class", params={"class_id": 4})
    response = client.get("/course/class", params={"course_id": 2})
    assert len(response.json()) == 2


def test_remove_course():
    response = client.delete("/course/", params={"course_id": 2})
    response = client.get("/course/", params={"course_id": 2})
    assert response.json() == []
