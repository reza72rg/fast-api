from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, route : str):
        self.detail= f"User not found in route {route}!!"
        self.status_code = status.HTTP_404_NOT_FOUND


class UserAlreadyExists(HTTPException):
    def __init__(self):
        self.detail = f"User already exists"
        self.status_code = status.HTTP_400_BAD_REQUEST