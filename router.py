from fastapi import APIRouter, Form, Depends, Response, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from utils import create_user, authenticate_user, get_current_user
from schemas import CreateUser, ResponseUser
from database import get_db
from models import DBUser

router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED)
def user_register(
        username: str = Form(),
        password: str = Form(),
        email: EmailStr = Form(),
        db: Session = Depends(get_db)
) -> dict:
    create_user(
        db=db,
        user=CreateUser(
            username=username,
            password=password,
            email=email
        )
    )
    return {"message": f"Hello, {username}! You have successfully registered!"}


@router.post("/login/", status_code=status.HTTP_200_OK)
def user_login(
        response: Response,
        username: str = Form(),
        password: str = Form(),
        db: Session = Depends(get_db)
) -> dict:
    access_token = authenticate_user(
        db=db,
        username=username,
        password=password
    )
    response.set_cookie("access_token", access_token, httponly=True)
    return {"message": f"Hello, {username}! You have successfully logged in!"}


@router.post("/logout/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def user_logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "You have been successfully logged out"}


@router.post("/me/", response_model=ResponseUser, status_code=status.HTTP_200_OK)
def get_me(current_user: DBUser = Depends(get_current_user)):
    return current_user
