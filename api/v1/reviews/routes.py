from fastapi import status, APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from api.v1.auth.dependency import AccessTokenBearer, CheckRole
from api.v1.reviews.models import Review
from api.v1.reviews.schema import ReviewCreateModel
from api.v1.reviews.service import ReviewService
from db.db import get_session


access_token_bearer = AccessTokenBearer()
role_checker = Depends(CheckRole(['admin', 'user']))

review_router = APIRouter()
review_service = ReviewService()


@review_router.post('/book/{book_uid}', status_code=status.HTTP_201_CREATED, response_model=Review, dependencies=[role_checker])
async def add_review_to_books(book_uid: str, review_data: ReviewCreateModel, session: AsyncSession = Depends(get_session), token_details=Depends(access_token_bearer)) -> Review:
    user_email = token_details['user']['email']
    new_review = await review_service.add_review_to_book(user_email=user_email, book_uid=book_uid, review_data=review_data, session=session)
    return new_review