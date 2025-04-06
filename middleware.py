import time

from fastapi import FastAPI, status
from fastapi.requests import Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware


def register_middleware(app: FastAPI):

    @app.middleware('http')
    async def custom_logging(request: Request, call_next):
        """Custom logging middleware that logs the time before and after handling the request."""

        start_time = time.time()
        print(f"--- Request Start ---\nTime: {start_time}\nPath: {request.url.path}")

        # Forward the request to the next middleware or route handler and await the response
        response = await call_next(request)

        end_time = time.time()
        duration = round(end_time - start_time, 4)
        print(f"--- Request End ---\nTime: {end_time}\nDuration: {duration} seconds\nPath: {request.url.path}")

        return response


    # @app.middleware('http')
    # async def authorization(request: Request, call_next):
    #     """middleware to check if Authorization header is present"""
    #
    #     if "authorization" not in request.headers:
    #         return JSONResponse(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             content={"detail": "Authorization header missing"}
    #         )
    #
    #     response = await call_next(request)
    #
    #     return response


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1"]
    )