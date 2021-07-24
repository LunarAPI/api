class ApiException(Exception):
    ...


class ManipulationError(ApiException):
    ...

class CouldNotReadImage(ApiException):
    ...


class BadRequest(ApiException):
    def __init__(self, msg: str):
        self.code = 400
        self.message = msg

    def __str__(self):
        return "BadRequest: {}: {}".format(self.code, self.message)