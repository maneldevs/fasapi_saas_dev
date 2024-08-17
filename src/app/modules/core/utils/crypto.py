from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt

from src.app.modules.core.utils.exceptions import TokenInvalidError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, secret: str, algorithm: str, expires_delta: timedelta | None = None):
    data_copy = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_copy.update({"exp": expire})
    encoded_jwt = jwt.encode(data_copy, secret, algorithm)
    return encoded_jwt


def decode_token(token: str, secret: str, algorithm: str) -> dict:
    payload = {}
    try:
        payload: dict = jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise TokenInvalidError("Token expired")
    except jwt.InvalidTokenError:
        raise TokenInvalidError
    return payload
