from datetime import date, datetime
import time

import boto3
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile, FileField
from django.forms import model_to_dict
from django_currentuser.middleware import get_current_user

from front.celery import app
import json

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


class LazyEncoder(DjangoJSONEncoder):
    """
    Funcao que permite o json.dumps converter corretamente os dicts que possuem campos com objects ImageField, e outros
    que forem necessários.
    # todo: objetos fk poderiam dar erro? lembrar de testar
    """
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            return str(obj)
        if isinstance(obj, FileField):
            return str(obj)
        return super().default(obj)


def monta_json_log(self):
    # registro = self.__dict__
    print("11111")
    registro = model_to_dict(self)

    print("22222")
    nome_model = self.__class__.__name__
    # pega usuario que salvou a alteracao
    print("33333")
    quem = get_current_user()
    registro['info_usuario'] = quem.username

    # pega data da alteração
    data = datetime.now()
    registro['info_data_modificado'] = data.strftime("%d/%m/%Y, %H:%M:%S")

    # nome do model
    registro['info_tabela'] = nome_model

    # remover campo desnecessário
    # del registro['_state']

    # converte dict em json str
    registro_str = ''
    try:
        registro_str = json.dumps(registro, ensure_ascii=False, cls=LazyEncoder)

    except Exception as e:
        print(e)
        registro_str = 'erro ao registrar log'

    return registro_str






def teste_cloud_log(obj):
    # chama funcao que formata o json com o registro alterado

    registro_str = monta_json_log(obj)

    # Todo: montar uma funcao celery para chamar a api do cloudwatch logs aqui:

    # instancia o cliente boto3 que acessa o servico cloudwatch-logs com as credenciais de um user com permissao
    logs = boto3.client('logs', region_name=settings.AWS_DEFAULT_REGION, aws_access_key_id=settings.CLOUDWATCH_AWS_ID,
                        aws_secret_access_key=settings.CLOUDWATCH_AWS_KEY)

    # nome do grupo: no tabelao será um só para cada inquilino
    LOG_GROUP = 'GROUP_CAFE'

    # nome do logStream => será mes/ano, virando o mes, novo logStream será criado dentro daquele logGroup
    data_hoje = date.today()
    data_hoje_str = data_hoje.strftime("%m/%Y")
    LOG_STREAM = data_hoje_str

    # Checa existencia do log Group, se nao existir, cria ele
    log_group_existe = logs.describe_log_groups(logGroupNamePrefix=LOG_GROUP)

    if len(log_group_existe['logGroups']) == 0:
        print("nao existe log group, CRIAR +++++++++++")
        logs.create_log_group(logGroupName=LOG_GROUP)

    # Checa existencia do log Stream , se nao existir, cria ele
    log_stream_existe = logs.describe_log_streams(logGroupName=LOG_GROUP, logStreamNamePrefix=LOG_STREAM)

    if len(log_stream_existe['logStreams']) == 0:
        print("nao existe log stream, CRIAR --------")
        logs.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)

    timestamp = int(round(time.time() * 1000)) # aqui bug
    # time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        print("o que TENEMOS aqui?")
        print(registro_str)

        response = logs.put_log_events(
            logGroupName=LOG_GROUP,
            logStreamName=LOG_STREAM,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': registro_str
                }
            ]
        )

    except logs.exceptions.InvalidSequenceTokenException as exception:

        sequence_token = exception.response['expectedSequenceToken']

        response = logs.put_log_events(
            logGroupName=LOG_GROUP,
            logStreamName=LOG_STREAM,
            sequenceToken=sequence_token,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': registro_str
                }
            ]
        )
# QUE BRANCH E ESSE? ASSINCRONA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
