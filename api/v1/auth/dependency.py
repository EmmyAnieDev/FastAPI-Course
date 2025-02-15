from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.requests import Request

from api.v1.auth.utils import decode_token

class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")

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
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token")


class RefreshTokenBearer(TokenBearer):
    @staticmethod
    def verify_token_data(token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a refresh token")