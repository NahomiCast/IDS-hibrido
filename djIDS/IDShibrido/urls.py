from django.urls import path
from IDShibrido.views import ingest_evento

urlpatterns = [
    path('events/', ingest_evento),
]