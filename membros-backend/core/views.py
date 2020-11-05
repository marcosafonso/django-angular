from django.shortcuts import render
from .models import Member, Event
from rest_framework import status, viewsets
from .serializers import MemberSerializer, MemberSimpleSerializer, EventSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import CafePermission
from rest_framework import filters as rest_filters


# teste django_filters
import django_filters
from django_filters import rest_framework as filters


class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')
    describe = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Event
        fields = ['name', 'describe']



# Create your views here. 
# isAuthenticated vai fazer a checagem se o user está autorizado pelo sistema de authentication
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [CafePermission]

    """Modificado para usar o serializer mais simples do Member model"""
    def list(self, request, *args, **kwargs):
        queryset = Member.objects.all()
        serializer = MemberSimpleSerializer(queryset, many=True)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    #authentication_classes = [TokenAuthentication, SessionAuthentication]
    #permission_classes = [IsAuthenticated]

    # testar filtro de campos
    filter_backends = (filters.DjangoFilterBackend, rest_filters.OrderingFilter)
    filterset_class = EventFilter
    ordering_fields = ('name',)
    ordering = ('-name',)

    def create(self, request, *args, **kwargs):
        msgs = {}
        dados = []
        for item in request.data:
            print(item)    
            serializer = self.get_serializer(data=item)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            msgs.update(headers)
            print(serializer.data)
            dados.append(serializer.data)

        return Response(dados, status=status.HTTP_201_CREATED, headers=msgs)
