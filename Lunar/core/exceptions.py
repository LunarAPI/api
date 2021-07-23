class ApiException(Exception):
    ...


class ManipulationError(ApiException):
    ...

class CouldNotReadImage(ApiException):
    ...


