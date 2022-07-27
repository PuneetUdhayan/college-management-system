# College Management System

College management system.

Note set up the environment variables required for the project by runnin the following command for windows

```
set SQLALCHAMY_DATABASE_URL=sqlite:///./college.db
```

## Running tests

Tests are written using pytest.
To run the tests use the command:

```
python -m pytest tests
```

To generate coverage run the following command:

```
python -m coverage run -m pytest tests
```

To output the report for the previously run coverage tests:

```
coverage report --omit=<environment_folder_name>/*
```

To export the report in HTML:

```
coverage html --omit=<environment_folder_name>/*
```

## To Do

- Add notification system
- Add authentication
- Add time slot check when assigning courses to students and teachers
- Improve test coverage