class BaseUserException(Exception):
    """
    Basic class for user exceptions
    """


class UserNotFoundException(BaseUserException):
    """
    Throw an exception when requested user not found
    """


class UserUnauthorizedException(BaseUserException):
    """
    Throw an exception wile user unauthorized
    """


class UserAlreadyAdminException(BaseUserException):
    """
    Throw an exception when user requested admin role while already being admin
    """
