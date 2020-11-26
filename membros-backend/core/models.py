import csv
from datetime import date, time

import boto3
import watchtower
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
import logging

# Create your models here.
from django.db.models.fields.files import ImageFieldFile
from django.forms import model_to_dict
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user
)
import json

from cria_log.funcoes import registra_log_event_pre_update, registra_log_event_pos_update
from front import settings


def processa_log(self):
    quem = get_current_user()
    registra_log_event_pos_update(self, quem)


def serialize(obj):
    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    return obj.__dict__


from datetime import datetime


# def registra_log_cloudwatch(self):
#     """
#     e lá vamos nós.
#     """
#     watchtower_handler = watchtower.CloudWatchLogHandler(log_group="Cake1", boto3_session=settings.logger_boto3_session)
#
#     registro = self.__dict__
#     nome_model = self.__class__.__name__
#     # pega usuario que salvou a alteracao
#     quem = get_current_user()
#     registro['info_usuario'] = quem.username
#
#     # pega data da alteração
#     data = datetime.now()
#     registro['info_data_modificado'] = data.strftime("%d/%m/%Y, %H:%M:%S")
#
#     # nome do model
#     registro['info_tabela'] = nome_model
#
#     # remover campo desnecessário
#     del registro['_state']
#
#     print(registro)
#
#     # envia para o cloudwatch log
#     logger = logging.getLogger("watchtower")
#     # logger.addHandler(watchtower_handler)
#     logger.info(registro)


# def ler_arquivo_s3(self):

    # registro = self.__dict__
    # nome_model = self.__class__.__name__
    # # pega usuario que salvou a alteracao
    # quem = get_current_user()
    # registro['info_usuario'] = quem.username
    #
    # # pega data da alteração
    # data = datetime.now()
    # registro['info_data_modificado'] = data.strftime("%d/%m/%Y, %H:%M:%S")
    #
    # # nome do model
    # registro['info_tabela'] = nome_model
    #
    # # remover campo desnecessário
    # del registro['_state']
#
#     obj_log = LogSistema.objects.filter().first()
#
#     if obj_log:
#         # fazer aqui
#         arquivo = obj_log.arquivo
#         arquivo.open(mode='a')
#
#         writer = csv.DictWriter(arquivo, fieldnames=['id', 'describe', 'info_usuario', 'name', 'info_tabela', 'info_data_modificado'])
#         writer.writerow(registro)
#
#         obj_log.arquivo = writer
#         obj_log.save()

import time
import json


class LazyEncoder(DjangoJSONEncoder):
    """
    Funcao que permite o json.dumps converter corretamente os dicts que possuem campos com objects ImageField, e outros
    que forem necessários.
    """
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            return str(obj)
        return super().default(obj)


def monta_json_log(self):

    # registro = self.__dict__
    registro = model_to_dict(self)

    nome_model = self.__class__.__name__
    # pega usuario que salvou a alteracao
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
    # todo: erro com imagefield not serializable
    registro_str = ''
    try:
        registro_str = json.dumps(registro, ensure_ascii=False, cls=LazyEncoder)

    except Exception as e:
        pass

    return registro_str


def teste_cloud_log(self):

    # chama funcao que formata o json com o registro alterado
    
    registro_str = monta_json_log(self)

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

    timestamp = int(round(time.time() * 1000))
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


# def busca_log_events(self):
#
#     # nome log group:
#     LOG_GROUP = 'GROUP_CAFE'
#
#     # nome do logStream => será mes/ano, virando o mes, novo logStream será criado dentro daquele logGroup
#     data_hoje = date.today()
#     data_hoje_str = data_hoje.strftime("%m/%Y")
#     LOG_STREAM = data_hoje_str
#
#     # instancia o cliente boto3 que acessa o servico cloudwatch-logs com as credenciais de um user com permissao
#     logs = boto3.client('logs', region_name=settings.AWS_DEFAULT_REGION, aws_access_key_id=settings.CLOUDWATCH_AWS_ID,
#                         aws_secret_access_key=settings.CLOUDWATCH_AWS_KEY)
#
#     # todo: teste de busca log_events:
#     response = logs.filter_log_events(
#         logGroupName=LOG_GROUP,
#         logStreamNames=[
#             LOG_STREAM,
#         ],
#         # logStreamNamePrefix='string', # prefix pesquisa por logstream que comecam com a str informada
#         # startTime=123,
#         # endTime=123,
#         # filterPattern='string',
#         # nextToken='string',
#         # limit=123,
#         # interleaved=True | False
#     )
#
#     # print("+++++++RESULTADO DA PESQUISA DE LOGS+++++++")
#     # print(response['events'][0]['message'])
#
#     for obj in response['events']:
#         print(obj)


class Member(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='members_profile', blank=True, null=True)
    data_modificacao = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        return self.name + ' - ' + self.phone

    def save(self, *args, **kwargs):
        super(Member, self).save(*args, **kwargs)
        teste_cloud_log(self)


class Event(models.Model):
    name = models.CharField(max_length=150)
    describe = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.describe

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        # registra_log_cloudwatch(self)
        # ler_arquivo_s3(self)
        teste_cloud_log(self)
        # busca_log_events(self)


class LogSistema(models.Model):
    arquivo = models.FileField(verbose_name='Arquivo')
    uploaded_at = models.DateTimeField(auto_now_add=True)


