import datetime

from django.test import TestCase
from django.urls import reverse

from core.models import Emprestimo, Member, Book


class EmprestimoViewTest(TestCase):

    def setUp(self):
        # criar objetos member e book
        member = Member.objects.create(name="Mario", surname="Andrade", phone="27-33219850",
                                       email="mario@andrade.com.br", address="av Central")
        book = Book.objects.create(nome="The Lion King", author="ValDisnei")

    def test_data_devolucao_maxima_correta(self):
        # testa se a validação permite corretamente data devolução de até 7 dias
        member = Member.objects.first()
        book = Book.objects.first()

        data_devolucao = datetime.date.today() + datetime.timedelta(days=7)

        corpo = {
            "data_emprestimo": "2021-06-04",
            "devolvido": True,
            "data_devolucao": data_devolucao,
            "member": int(member.id),
            "book": int(book.id)
        }

        response = self.client.post('/emprestimos/', data=corpo)

        self.assertEqual(response.status_code, 201)

    def test_data_devolucao_maxima_invalida(self):
        # testa se a validação está devidamente impedindo data devolução maior que 7 dias
        member = Member.objects.first()
        book = Book.objects.first()

        data_devolucao = datetime.date.today() + datetime.timedelta(days=8)

        corpo = {
            "data_emprestimo": "2021-06-04",
            "devolvido": True,
            "data_devolucao": data_devolucao,
            "member": int(member.id),
            "book": int(book.id)
        }

        response = self.client.post('/emprestimos/', data=corpo)

        self.assertEqual(response.status_code, 400)

    def test_data_devolucao_esta_no_passado(self):
        # testa se a validação está devidamente impedindo data devolução anterior ao dia atual
        member = Member.objects.first()
        book = Book.objects.first()

        data_devolucao = datetime.date.today() - datetime.timedelta(days=1)

        corpo = {
            "data_emprestimo": "2021-06-04",
            "devolvido": True,
            "data_devolucao": data_devolucao,
            "member": int(member.id),
            "book": int(book.id)
        }

        response = self.client.post('/emprestimos/', data=corpo)
        self.assertEqual(response.status_code, 400)
