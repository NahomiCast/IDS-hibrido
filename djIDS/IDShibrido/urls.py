from django.urls import path
from .views import ingest_evento

urlpatterns = [
    path('events/', ingest_evento),
]