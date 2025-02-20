import uuid
from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import User
from .schema import UserCreateModel
from .utils import generate_password_hash


class UserService:

    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user


    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False


    @staticmethod
    async def create_user_account(user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()  # Convert to dictionary
        new_user = User(**user_data_dict, uid=uuid.uuid4(), created_at=datetime.now(), updated_at=datetime.now())
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        session.add(new_user)
        await session.commit()
        return new_user