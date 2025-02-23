from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Review
from .schema import ReviewCreateModel
from ..auth.service import UserService
from ..books.service import BookService

user_service = UserService()
book_service = BookService()


class ReviewService:

    @staticmethod
    async def add_review_to_book(user_email: str, book_uid: str, review_data: ReviewCreateModel, session: AsyncSession) -> Review:
        user = await user_service.get_user_by_email(email=user_email, session=session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        book = await book_service.get_book(book_uid=book_uid, session=session)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

        try:
            new_review = Review(**review_data.model_dump(), user=user, book=book)

            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)

            return new_review

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while adding the review.")