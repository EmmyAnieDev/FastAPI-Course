from datetime import timedelta, datetime

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from api.v1.auth.dependency import RefreshTokenBearer, AccessTokenBearer, get_current_user, CheckRole
from api.v1.auth.models import User
from api.v1.auth.schema import UserCreateModel, UserLoginModel, UserModel
from api.v1.auth.service import UserService
from api.v1.auth.utils import verify_password, create_access_token
from db.db import get_session
from db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_checker = CheckRole(['admin', 'user'])


@auth_router.post('/signup', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    user_email = user_data.email
    user_exists = await user_service.user_exists(user_email, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exists")

    new_user = await user_service.create_user_account(user_data, session)
    return new_user


@auth_router.post('/login', response_model=User, status_code=status.HTTP_200_OK)
async def login_user_account(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")

    access_token = create_access_token(
        user_data={
            'email': user.email,
            'user_uid': str(user.uid),
            'role': user.role
        }
    )

    refresh_token = create_access_token(
        user_data={
            'email': user.email,
            'user_uid': str(user.uid),
        },
        expiry=timedelta(days=2),
        refresh=True
    )

    # Convert the user model to JSON serializable format
    user_data = jsonable_encoder(user)

    return JSONResponse(
        content={
            "message": "Login Successful",
            "user": user_data,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )


@auth_router.get('/refresh_token', status_code=status.HTTP_200_OK)
async def create_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):

    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) <= datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token expired")

    new_access_token = create_access_token(
        user_data={
            'email': token_details['user']['email'],
            'user_uid': str(token_details['user']['user_uid']),
            'role': str(token_details['user']['role']),
        }
    )

    new_refresh_token = create_access_token(
        user_data={
            'email': token_details['user']['email'],
            'user_uid': str(token_details['user']['user_uid']),
        },
        expiry=timedelta(days=2),
        refresh=True
    )

    return JSONResponse(
        content={
            "message": "New Tokens Created",
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
    )


@auth_router.get('/user', status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_current_user_account(current_user: dict = Depends(get_current_user), _: bool = Depends(role_checker)):
    return current_user


@auth_router.post('/logout', status_code=status.HTTP_200_OK)
async def logout_user_account(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)

    return JSONResponse(content={"message": "Logged out Successfully"})