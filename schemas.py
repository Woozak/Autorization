from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr


class CreateUser(BaseUser):
    password: str


class ResponseUser(BaseUser):
    id: int
