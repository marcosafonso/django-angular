from datetime import date

import watchtower
from django.db import models
import logging

# Create your models here.
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


def registra_log_cloudwatch(self):
    """
    e lá vamos nós.
    """
    watchtower_handler = watchtower.CloudWatchLogHandler(log_group="Cake1", boto3_session=settings.logger_boto3_session)

    registro = self.__dict__
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
    del registro['_state']

    print(registro)

    # envia para o cloudwatch log
    logger = logging.getLogger("watchtower")
    logger.addHandler(watchtower_handler)
    logger.info(registro)


# def ler_arquivo_s3(self):
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
#     obj_log = LogSistema.objects.filter().first()
#
#     if obj_log:
#         pass
        # arquivo = obj_log.arquivo
        #
        # arquivo.open(mode="r")
        # content = arquivo.read()
        # # lines = arquivo.readlines()
        #
        # a.write(registro)
        #
        # obj_log.arquivo = a
        # obj_log.save()
        #
        # arquivo.close()


class Member(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='members_profile', blank=True, null=True)

    def __str__(self):
        return self.name + ' - ' + self.phone

    def save(self, *args, **kwargs):
        super(Member, self).save(*args, **kwargs)
        registra_log_cloudwatch(self)


class Event(models.Model):
    name = models.CharField(max_length=150)
    describe = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.describe

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        registra_log_cloudwatch(self)
        # ler_arquivo_s3(self)


class LogSistema(models.Model):
    arquivo = models.FileField(verbose_name='Arquivo')
    uploaded_at = models.DateTimeField(auto_now_add=True)


