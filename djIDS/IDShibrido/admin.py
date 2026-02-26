from django.contrib import admin
from IDShibrido.models import Evento

# Register your models here.
#admin.site.register(Evento)
from django.contrib import admin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'source_ip',
        'destination_port',
        'protocol',
        'action',
    )
    list_filter = ('protocol', 'action')
    search_fields = ('source_ip',)
