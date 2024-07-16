import jwt
from fastapi import Request, Depends
from sqlalchemy.orm import Session

import exceptions
from auth.security import get_password_hash, verify_password, create_access_token
from auth.config import config, read_public_key
from schemas import CreateUser
from database import get_db
from models import DBUser


def check_username_and_email_in_db(db: Session, username: str, email: str):
    user = db.query(DBUser).filter(DBUser.username == username or DBUser.email == email).first()
    if user:
        if user.username == username:
            raise exceptions.UsernameAlreadyRegisteredException
        if user.email == email:
            raise exceptions.EmailAlreadyRegistered


def create_user(db: Session, user: CreateUser) -> DBUser:
    check_username_and_email_in_db(db, user.username, user.email)
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_from_db(db: Session, username: str):
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if not user:
        raise exceptions.InvalidUsernameOrPassword
    return user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_from_db(db=db, username=username)
    password_is_valid = verify_password(password, user.hashed_password)
    if not password_is_valid:
        raise exceptions.InvalidUsernameOrPassword
    access_token = create_access_token({"sub": user.username})
    return access_token


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise exceptions.NotAuthorized
    return token


def get_current_user(db: Session = Depends(get_db), token: str = Depends(get_token)):
    public_key = read_public_key()
    payload = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[config.algorithm]
    )
    username = payload.get("sub")
    user = get_user_from_db(db=db, username=username)
    if not user:
        raise exceptions.UserNotFound
    return user
