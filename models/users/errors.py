class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistError(Exception):
    def __init__(self, message):
        self.message = message


class IncorrectPasswordError(Exception):
    def __init__(self, message):
        self.message = message
