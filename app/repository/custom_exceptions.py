class StudentNotFound(Exception):

    def __init__(self):
        super().__init__('No student found for the given student ID')


class CourseNotFound(Exception):

    def __init__(self):
        super().__init__('Course not found for the given inputs')


class IncorrectDayOfWeek(Exception):

    def __init__(self):
        super().__init__('Day of week not found. Check the format.')