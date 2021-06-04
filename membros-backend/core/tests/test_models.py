from django.test import TestCase
from core.models import Member, Event

# Create your tests here.


class MemberTestCase(TestCase):

    def setUp(self):
        Member.objects.create(name='Marcos Alonso', surname="Silves", phone="2733218600",
                              email="alonso@chelsea.com", address="Av Street")

    def teste_metodos_member(self):
        member = Member.objects.first()

        # caso erro
        # self.assertEqual(member.hello_member(), 'Welcome Marcos Alonso2')
        # caso certo
        self.assertEqual(member.hello_member(), 'Welcome Marcos Alonso')

        self.assertEqual(member.email, "alonso@chelsea.com")

        self.assertEqual(member.soma_numeros(10, 5), 15)

        self.assertEqual(member.calcula_porcentagem_de_valor(300, 600), 50)
