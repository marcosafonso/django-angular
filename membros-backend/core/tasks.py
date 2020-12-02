from celery.utils.log import get_task_logger
from django.conf import settings

from front.celery import app

logger = get_task_logger(__name__)


# @app.task(name="send_confirmation_email_task")
# def send_confirmation_email(token, id, email):
#     logger.info('Creating the task..')
#
#     subject = 'Obrigado por se cadastrar!'
#     from_email = settings.EMAIL_HOST_USER
#     message = f"http://localhost:8000/confirm/?confirmation_key={token}&id={id}"
#     to = email
#
#     send_mail(
#         subject,
#         message,
#         from_email,
#         [to],
#         fail_silently=False,
#     )
#
#     logger.info('Finishing task..')


@app.task(name="ola_mundo_task")
def ola_mundo_task():
    logger.info('Fazendo teste 0001 alfa..')

    cont = 0
    while cont < 20:
        print("conta: ", cont)
        cont = cont + 1

    logger.info('Finishing task..')
