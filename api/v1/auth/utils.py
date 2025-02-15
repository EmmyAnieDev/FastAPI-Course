import logging
import uuid
from datetime import timedelta, datetime

import jwt
from passlib.context import CryptContext

from config import Config

password_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    hashed_password = password_context.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {
        'user': user_data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }

    token = jwt.encode(
        algorithm=Config.JWT_ALGORITHM,
        payload=payload,
        key=Config.JWT_SECRET
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            algorithms=[Config.JWT_ALGORITHM],
            jwt=token,
            key=Config.JWT_SECRET
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None