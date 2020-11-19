from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
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


