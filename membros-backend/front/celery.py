from __future__ import absolute_import, unicode_literals

import logging
import os

from celery import Celery
from django.conf import settings

logger = logging.getLogger("Celery")


# define o módulo de configurações padrão do Django para o 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'front.settings')

app = Celery('front')


# Usando uma string aqui significa que o 'worker' não precisa serializar
# o objeto de configuração para processos filhos.
# O namespace = 'CELERY' significa todas as chaves de configuração
# relacionadas ao celery deve ter um prefixo `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Carrega os módulos de tasks de todas as configurações registradas
# da aplicação Django.
app.autodiscover_tasks()

# Só pra debug
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
