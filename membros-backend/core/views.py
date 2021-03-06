from datetime import date

import boto3
from django.http import HttpResponse
from django.views import View
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from front import settings
from .models import Member, Event, Book, Emprestimo
from rest_framework import status, viewsets
from .serializers import MemberSerializer, EventSerializer, MemberSimpleSerializer, BookSerializer, EmprestimoSerializer
from rest_framework import filters as rest_filters


# teste django_filters
import django_filters
from django_filters import rest_framework as filters


class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith', distinct=True)
    describe = django_filters.CharFilter(lookup_expr='istartswith', distinct=True)

    class Meta:
        model = Event
        fields = "__all__"


# Create your views here. 
# isAuthenticated vai fazer a checagem se o user está autorizado pelo sistema de authentication
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend, rest_filters.OrderingFilter, rest_filters.SearchFilter)
    # metodo ninja do search fields
    search_fields = [f.get_attname() for f in Member._meta.fields]

    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [CafePermission]

    # """Modificado para usar o serializer mais simples do Member model"""
    # def list(self, request, *args, **kwargs):
    #     queryset = Member.objects.all()
    #     serializer = MemberSimpleSerializer(queryset, many=True)
    #     return Response(serializer.data)


import logging


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    # testar filtro de campos
    filter_backends = (filters.DjangoFilterBackend, rest_filters.OrderingFilter, rest_filters.SearchFilter)
    # metodo ninja do search fields
    search_fields = [f.get_attname() for f in Event._meta.fields]

    # filterset_class = EventFilter
    ordering_fields = ('name',)
    ordering = ('-name',)

    # todo: parei em logger direto pro cloud
    # teste de registrar log no cloudwatch
    # def perform_create(self, serializer):
    #     event = serializer.save()
    #     # Log our new student


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer


@api_view(['GET'])
def view_log_events(request):
    """
    Busca registros de log do CloudWatch aws.
    :param request:
    :return:
    """
    # nome log group:
    LOG_GROUP = 'GROUP_CAFE'

    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        body_data = body_data['mes/ano']
        print(body_data)

    except Exception as e:
        msg = {'Retorno': 'dados Informados não estão no formato { "mes/ano": "mm/yyyy" } (mes/ano).'}
        return Response(msg, content_type='application/json')


    # nome do logStream => será mes/ano, virando o mes, novo logStream será criado dentro daquele logGroup
    data_hoje = date.today()
    data_hoje_str = data_hoje.strftime("%m/%Y")
    LOG_STREAM = body_data

    # instancia o cliente boto3 que acessa o servico cloudwatch-logs com as credenciais de um user com permissao
    logs = boto3.client('logs', region_name=settings.AWS_DEFAULT_REGION, aws_access_key_id=settings.CLOUDWATCH_AWS_ID,
                        aws_secret_access_key=settings.CLOUDWATCH_AWS_KEY)

    try:
        response = logs.filter_log_events(
            logGroupName=LOG_GROUP,
            logStreamNames=[
                LOG_STREAM,
            ],
            # logStreamNamePrefix='string', # prefix pesquisa por logstream que comecam com a str informada
            # startTime=123,
            # endTime=123,
            # filterPattern='string',
            # nextToken='string',
            # limit=123,
            # interleaved=True | False
        )

    except logs.exceptions.ResourceNotFoundException:
        msg = {'Retorno': 'Não há registros de log disponíveis para consulta.'}
        return Response(msg, content_type='application/json')

    # for obj in response['events']:
    #     print(obj)
    # j = json.dumps(response)

    # pega valor da qtd de logs retornados
    qtd_logs = len(response['events'])

    # na response, a chave events contém os logs
    events = response['events']

    cont = 0
    list_logs = []
    # Iterar sobre os logs pegando apenas a informacao de alteracao, e adicionando na list_logs
    while cont < qtd_logs:
        # pegar só o campo message de cada log retornado, pois message contem a fotografia da alteracao do model
        str_message = events[cont]['message']
        # converte str message em python obj
        object_message = json.loads(str_message)

        list_logs.append(object_message)
        cont = cont + 1

    # json_str = json.dumps(response['events'], ensure_ascii=False)
    # json_object = json.loads(json_str)

    return Response(list_logs, content_type='application/json')

from .tasks import ola_mundo_task
from django.contrib import messages


class OlaMundoView(View):

    def get(self, request):

        ola_mundo_task.delay()

        messages.success(request, 'Olá Mundo realizado com sucesso!')

        return HttpResponse("Não há vagas!")
