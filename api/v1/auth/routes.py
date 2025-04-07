from datetime import timedelta, datetime

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from api.v1.auth.dependency import RefreshTokenBearer, AccessTokenBearer, get_current_user, CheckRole
from api.v1.auth.models import User
from api.v1.auth.schema import UserCreateModel, UserLoginModel, UserModel, EmailModel
from api.v1.auth.service import UserService
from api.v1.auth.utils import verify_password, create_access_token, create_url_safe_token, decode_url_safe_token
from config import Config
from db.db import get_session
from db.redis import add_jti_to_blocklist
from errors import UserAlreadyExists, UserNotFound, IncorrectPassword, RefreshTokenExpired
from mail import create_message, mail

auth_router = APIRouter()
user_service = UserService()
role_checker = CheckRole(['admin', 'user'])


@auth_router.post('/send-mail', status_code=status.HTTP_200_OK)
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the App</h1>"

    message = create_message(
        recipients=emails,
        subject="Welcome",
        body=html
    )

    await mail.send_message(message)

    return {"message": "Email sent successfully!"}


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    user_email = user_data.email
    user_exists = await user_service.user_exists(user_email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user_account(user_data, session)

    token = create_url_safe_token({"email": user_email})

    link = f"http://{Config.DOMAIN_NAME}/api/v1/auth/verify/{token}"

    account_verification_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    message = create_message(
        recipients=[user_email],
        subject="Welcome, Verify your email",
        body=account_verification_message
    )

    await mail.send_message(message)

    return {
        "message": "Account created please verify your email",
        "user": new_user
    }


@auth_router.get('/verify/{token}')
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK
        )

    return JSONResponse(
        content={"message": "Error during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@auth_router.post('/login', response_model=User, status_code=status.HTTP_200_OK)
async def login_user_account(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise UserNotFound()

    if not verify_password(password, user.password_hash):
        raise IncorrectPassword()

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
        raise RefreshTokenExpired()

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