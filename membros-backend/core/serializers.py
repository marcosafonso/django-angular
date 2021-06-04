import datetime

from rest_framework import serializers
from .models import Member, Event, Book, Emprestimo


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['id', 'name', 'surname', 'phone', 'photo', 'data_modificacao']


class MemberSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'surname', 'phone']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'describe']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = "__all__"

    # caso 1 - validar apenas um campo de forma customizada, usar metodo 'validate_<nome_campo>'
    def validate_data_devolucao(self, value):
        """
        Checar, caso usuario informou data devolução no passado.
        """
        if value < datetime.date.today():
            raise serializers.ValidationError("Oh not! Data está no passado.")

        # checar se data está no intervalo permitido (até 1 semana no futuro).
        if value > datetime.date.today() + datetime.timedelta(weeks=1):
            raise serializers.ValidationError('Data inválida - Devolução deve ocorrer em até 7 dias.')

        return value

    # caso 2 - validação que envolve mais de um campo, usar metodo 'validate'
    # def validate(self, data):
    #     """
    #     Check that start is before finish.
    #     """
    #     if data['start'] > data['finish']:
    #         raise serializers.ValidationError("finish must occur after start")
    #     return data
