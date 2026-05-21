from django.urls import path
from .views import ingest_evento
from .views import ingest_evento, dashboard
from .views import (
    ingest_evento,
    dashboard,
    alerts_view,
    events_view
)

urlpatterns = [
    path('events/', ingest_evento),
    path('dashboard/', dashboard),
    path('alerts/', alerts_view),
    path('traffic/', events_view),
]
