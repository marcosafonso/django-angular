from django.contrib import admin
from .models import Member, Event, LogSistema, Book, Emprestimo
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Permission)
admin.site.register(LogSistema)
admin.site.register(Book)
admin.site.register(Emprestimo)
