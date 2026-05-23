from django.contrib import admin

from .models import (
    Evento,
    Alerta,
    RuleConfig
)


# =========================
# EVENTOS
# =========================

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):

    list_display = (
        'timestamp',
        'source_ip',
        'destination_port',
        'protocol',
        'action'
    )

    search_fields = (
        'source_ip',
        'protocol',
        'action'
    )

    list_filter = (
        'protocol',
        'action'
    )

    ordering = ('-timestamp',)


# =========================
# ALERTAS
# =========================

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):

    list_display = (
        'timestamp',
        'alert_type',
        'source_ip',
        'severity'
    )

    search_fields = (
        'source_ip',
        'alert_type'
    )

    list_filter = (
        'severity',
        'alert_type'
    )

    ordering = ('-timestamp',)


# =========================
# RULE CONFIG
# =========================

@admin.register(RuleConfig)
class RuleConfigAdmin(admin.ModelAdmin):

    list_display = (
        'key',
        'value',
        'description'
    )

    search_fields = (
        'key',
    )


