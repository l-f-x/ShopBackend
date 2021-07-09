class InvalidTokenException(Exception):
    def __init__(self, name: str):
        self.name = name


class InvalidPasswordException(Exception):
    def __init__(self, name: str):
        self.name = name


class EmailUsedException(Exception):
    def __init__(self, name: str):
        self.name = name


class TokenExpireException(Exception):
    def __init__(self, name: str):
        self.name = name
