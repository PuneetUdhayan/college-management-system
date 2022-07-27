class StudentNotFound(Exception):

    def __init__(self):
        super().__init__('No student found for the given student ID')