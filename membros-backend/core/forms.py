import datetime

from django import forms


class DevolucaoBookForm(forms.Form):
    """Form for a librarian to renew books."""
    data_devolucao = forms.DateField(help_text="Data de agora até 4 semanas.")

    def clean_data_devolucao(self):
        data = self.cleaned_data['data_devolucao']

        # Checar se data não é do passado
        if data < datetime.date.today():
            raise forms.ValidationError('Data inválida - devolução no passado')

        # checar se data está no intervalo permitido (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise forms.ValidationError('Data inválida - ultrapassou 4 semanas para devolução')
        # Remember to always return the cleaned data.
        return data
