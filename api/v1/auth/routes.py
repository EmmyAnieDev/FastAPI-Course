from typing import List
from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from api.v1.auth.models import User
from api.v1.auth.schema import UserCreateModel
from api.v1.auth.service import UserService
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