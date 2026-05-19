from django.urls import path
from .views import ingest_evento
from .views import ingest_evento, dashboard

urlpatterns = [
    path('events/', ingest_evento),
    path('dashboard/', dashboard),
]

