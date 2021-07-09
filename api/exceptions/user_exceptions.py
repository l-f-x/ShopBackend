class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


class AccessDeniedException(Exception):
    def __init__(self, name: str):
        self.name = name
