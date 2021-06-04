from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from core.models import Event, teste_cloud_log
from cria_log.funcoes import registra_log_event, registra_log_event_pre_update
from .tasks import teste_cloud_log
from .models import Event

# @receiver(post_save, sender=Event)
# def create_event(sender, instance, created, **kwargs):
#     if created:
#         print("=== temos um signal LOG funcionando ===")
#         registra_log_event(instance)
#
#

# @receiver(pre_save, sender=Event)
# def update_event(sender, instance, **kwargs):
#     """
#         Pegar valor antes e depois da alteracao e registrar em arquivo log.
#     """
#
#     # se está sendo atualizado, entao capturar o valor antes da alteração ser efetuada
#     if instance.id:
#         old_event = Event.objects.get(pk=instance.id)
#         print("vamos ver o antes e depois")
#         registra_log_event_pre_update(old_event, instance)
#         print("ja gerou old new !!")
#


# @receiver(post_save, sender=Event)
# def save_events(sender, instance, **kwargs):
#     """
#     Event is called for every [CREATE, UPDATE] on EVENTS table
#     :param sender:
#     :param instance: Instance of the EVENTS model
#     :param kwargs:
#     :return:
#     """
#     print("=======Churrasco?")
#
#     # TODO: nao funciona, pq nao funciona????
#     teste_cloud_log.delay(obj=instance)
#     print("=======Mister cook?")

@receiver(post_save, sender=Event)
def update_event(sender, instance, **kwargs):
    """
        Pegar valor antes e depois da alteracao e registrar em arquivo log.
    """

    # se está sendo atualizado, entao capturar o valor antes da alteração ser efetuada
    if instance.id:
        old_event = Event.objects.get(pk=instance.id)
        print("vamos ver o antes e depois")
        # teste_cloud_log(instance)
        print("ja gerou old new !!")

