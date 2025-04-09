from celery import Celery
from config import Config

celery_app = Celery(
    "worker",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
    imports=[
        "api.v1.auth.celery_send_email"  # The module with your @celery_app.task
    ],
)