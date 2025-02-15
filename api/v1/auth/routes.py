from datetime import timedelta

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from api.v1.auth.models import User
from api.v1.auth.schema import UserCreateModel, UserLoginModel
from api.v1.auth.service import UserService
from api.v1.auth.utils import verify_password, create_access_token
from db.db import get_session

user_router = APIRouter()
user_service = UserService()


@user_router.post('/signup', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    user_email = user_data.email
    user_exists = await user_service.user_exists(user_email, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exists")

    new_user = await user_service.create_user_account(user_data, session)
    return new_user


@user_router.post('/login', response_model=User, status_code=status.HTTP_200_OK)
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