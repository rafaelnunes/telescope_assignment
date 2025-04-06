class TelescopeException(Exception):
    pass


class TelescopeValidationException(Exception):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg


class ObjectNotFound(TelescopeException):
    pass
