class StudentNotFound(Exception):

    def __init__(self):
        super().__init__('No student found for the given student ID')


class TeacherNotFound(Exception):

    def __init__(self):
        super().__init__('No teacher found for the given teacher ID')


class CourseNotFound(Exception):

    def __init__(self):
        super().__init__('Course not found for the given inputs')


class ClassNotFound(Exception):

    def __init__(self):
        super().__init__('Class not found for the given inputs')


class IncorrectDayOfWeek(Exception):

    def __init__(self):
        super().__init__('Day of week not found. Check the format.')