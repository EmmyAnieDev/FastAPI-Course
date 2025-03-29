from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class BooklyException(Exception):
    """This is the base class for all bookly errors"""

    pass


class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(BooklyException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(BooklyException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(BooklyException):
    """User has provided an access token when a refresh token is needed"""

    pass


class RefreshTokenExpired(BooklyException):
    """Refresh token has expired. Please log in again."""

    pass


class UserAlreadyExists(BooklyException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(BooklyException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class BookNotFound(BooklyException):
    """Book Not found"""

    pass


class UserNotFound(BooklyException):
    """User Not found"""

    pass


class IncorrectPassword(BooklyException):
    """password not correct"""

    pass


class AccountNotVerified(Exception):
    """Account not yet verified"""
    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: BooklyException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "status_code": status.HTTP_403_FORBIDDEN,
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        ),
    )
    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "status_code": status.HTTP_400_BAD_REQUEST,
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "status_code": status.HTTP_401_UNAUTHORIZED,
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "status_code": status.HTTP_401_UNAUTHORIZED,
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "status_code": status.HTTP_401_UNAUTHORIZED,
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get a refresh token",
                "status_code": status.HTTP_403_FORBIDDEN,
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenExpired,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get a valid refresh token or login again",
                "status_code": status.HTTP_400_BAD_REQUEST,
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "status_code": status.HTTP_401_UNAUTHORIZED,
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book Not Found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not verified",
                "error_code": "account_not_verified",
                "status_code": status.HTTP_403_FORBIDDEN,
            },
        ),
    )

    app.add_exception_handler(
        IncorrectPassword,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Password Not correct",
                "error_code": "provide correct password or change password",
                "status_code": status.HTTP_401_UNAUTHORIZED,
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )