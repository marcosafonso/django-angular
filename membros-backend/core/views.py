from datetime import date

import boto3
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from front import settings
from .models import Member, Event
from rest_framework import status, viewsets
from .serializers import MemberSerializer, EventSerializer
from rest_framework import filters as rest_filters


# teste django_filters
import django_filters
from django_filters import rest_framework as filters


class EventFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='istartswith')
    # describe = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Event
        fields = "__all__"


# Create your views here. 
# isAuthenticated vai fazer a checagem se o user está autorizado pelo sistema de authentication
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

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
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
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

@api_view(['GET'])
def view_log_events(request):
    # nome log group:
    LOG_GROUP = 'GROUP_CAFE'

    # nome do logStream => será mes/ano, virando o mes, novo logStream será criado dentro daquele logGroup
    data_hoje = date.today()
    data_hoje_str = data_hoje.strftime("%m/%Y")
    LOG_STREAM = data_hoje_str

    # instancia o cliente boto3 que acessa o servico cloudwatch-logs com as credenciais de um user com permissao
    logs = boto3.client('logs', region_name=settings.AWS_DEFAULT_REGION, aws_access_key_id=settings.CLOUDWATCH_AWS_ID,
                        aws_secret_access_key=settings.CLOUDWATCH_AWS_KEY)

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

    # for obj in response['events']:
    #     print(obj)
    # j = json.dumps(response)
    print(type(response))

    # convert dicionario response em json str
    json_str = json.dumps(response['events'], ensure_ascii=False)
    json_object = json.loads(json_str)

    return Response(json_object, content_type='application/json')
