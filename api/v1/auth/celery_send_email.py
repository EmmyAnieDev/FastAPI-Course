from celery_conf import celery_app
from mail import create_message, send_message_sync


@celery_app.task()
def send_email(recipients: list[str], subject: str, body: str):

    message = create_message(
        recipients=recipients,
        subject=subject,
        body=body
    )

    send_message_sync(message)