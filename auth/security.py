import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from auth.config import config, read_private_key


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    payload = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=30)
    payload.update(
        {"iat": now,
         "exp": expire}
    )
    private_key = read_private_key()
    access_token = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=config.algorithm
    )
    return access_token
