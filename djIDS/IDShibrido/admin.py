from django.contrib import admin
from .models import Evento, Alerta

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'source_ip', 'destination_port', 'protocol', 'action')


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'source_ip', 'alert_type', 'severity')
