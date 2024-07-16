from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code = 400
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UsernameAlreadyRegisteredException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Username already registered"


class EmailAlreadyRegistered(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Email already registered"


class InvalidUsernameOrPassword(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid username or password"


class NotAuthorized(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "You are not authorized"


class UserNotFound(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User not found"
