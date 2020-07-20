from django.shortcuts import render
from .models import Member
from rest_framework import status, viewsets
from .serializers import MemberSerializer, MemberSimpleSerializer
from rest_framework.response import Response

# Create your views here.
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    """Modificado para usar o serializer mais simples do Member model"""
    def list(self, request, *args, **kwargs):
        queryset = Member.objects.all()
        serializer = MemberSimpleSerializer(queryset, many=True)
        return Response(serializer.data)
