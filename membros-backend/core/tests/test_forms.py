import datetime

from django.test import TestCase
from django.utils import timezone

from core.forms import DevolucaoBookForm


class DevolucaoBookFormTest(TestCase):

    def test_data_devolucao_no_passado(self):
        # testa se data devolucao está no passado em relação ao dia atual
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = DevolucaoBookForm(data={'data_devolucao': date})
        self.assertEqual(form.is_valid(), False)

    def test_data_devolucao_alem_do_tempo(self):
        # data devolução não deve exceder 4 semanas apos hoje
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = DevolucaoBookForm(data={'data_devolucao': date})
        self.assertEqual(form.is_valid(), True)
