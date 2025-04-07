from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from fastapi.requests import Request
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Any

from api.v1.auth.models import User
from api.v1.auth.service import UserService
from api.v1.auth.utils import decode_token
from db.db import get_session
from db.redis import jti_in_blocklist
from errors import AccessTokenRequired, RefreshTokenRequired, InvalidToken, RevokedToken, InsufficientPermission, \
    AccountNotVerified


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    # Allow creating an object from a class, enabling it to be called like a function (e.g., Depends(AccessTokenBearer())).
    # Allow us create dependencies and then call them as functions.
    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise InvalidToken()

        if await jti_in_blocklist(token_data['jti']):
            raise RevokedToken()

        self.verify_token_data(token_data)

        return token_data

    @staticmethod
    def token_valid(token: str) -> bool:
        token_data = decode_token(token)
        return bool(token_data)

    @staticmethod
    def verify_token_data(token_data):
        raise NotImplementedError("Please override this method in child classes")


class AccessTokenBearer(TokenBearer):
    @staticmethod
    def verify_token_data(token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    @staticmethod
    def verify_token_data(token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired


async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    user_email = token_details['user']['email']
    user = await UserService.get_user_by_email(user_email, session)
    return user


class CheckRole:

    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if not current_user.is_verified:
            raise AccountNotVerified

        if current_user.role in self.allowed_roles:
            return True

        raise InsufficientPermission()