

"""
    todo: Criar funcao que executa e cria um csv de log do django, a cada alteração;
    Passos:
    1 - encontrar libs e métodos necessários;
    2 - Montar função de teste no create/update;
    3 - Validar

"""
import csv


def minha_funcao():

    with open('movies.csv', 'w+', encoding='utf-8') as arquivo_csv:

        colunas = ['nome', 'rating']

        escrever = csv.DictWriter(arquivo_csv, fieldnames=colunas, delimiter=',', lineterminator='\n')

        escrever.writeheader()

        escrever.writerow({'nome': 'A Origem', 'rating': '94'})
        escrever.writerow({'nome': 'John Wick: Parabellum', 'rating': '84'})
        escrever.writerow({'nome': 'Vingadores: Guerra Infinita', 'rating': '97'})
        escrever.writerow({'nome': 'Até o Ultimo Homem', 'rating': '96'})


def registra_log_event(event):
    if event:
        with open('events_log.csv', 'a+', encoding='utf-8') as arquivo_csv:

            colunas = ['nome', 'describe']

            escrever = csv.DictWriter(arquivo_csv, fieldnames=colunas, delimiter=',', lineterminator='\n')

            escrever.writeheader()

            escrever.writerow({'nome': event.name, 'describe': event.describe})




def registra_log_event_pre_update(event_new):

    with open('events_log_pre_saves.csv', 'a+', encoding='utf-8') as arquivo_csv:

        colunas = ['id', 'name', 'describe', 'status', 'user']

        escrever = csv.DictWriter(arquivo_csv, fieldnames=colunas, delimiter=',', lineterminator='\n')

        escrever.writeheader()

        escrever.writerow({'id': event_new.id, 'name': event_new.name,
                           'describe': event_new.describe,
                           'status': 'pré-save', 'user': ' - '})




def registra_log_event_pos_update(event_new, user):

    # todo: continuar escrevendo no mesmo arquivo durante um tempo específico

    with open('events_log_pre_saves.csv', 'a+', encoding='utf-8') as arquivo_csv:

        colunas = ['id', 'tabela', 'name', 'describe', 'status', 'user']
        # colunas = [f.get_attname() for f in 'Event'._meta.fields]

        escrever = csv.DictWriter(arquivo_csv, fieldnames=colunas, delimiter=',', lineterminator='\n')

        if arquivo_csv.tell() == 0:
            escrever.writeheader()

        # escrever.writeheader()

        nome_model = event_new.__class__.__name__

        escrever.writerow({'id': event_new.id, 'tabela': nome_model, 'name': event_new.name,
                           'describe': event_new.describe,
                           'status': 'pós-save', 'user': user.username})

