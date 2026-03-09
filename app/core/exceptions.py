class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, resource: str, id: int):
        super().__init__(f"{resource} with id={id} not found.", status_code=404)


class ConflictException(AppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class UnprocessableException(AppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=422)
