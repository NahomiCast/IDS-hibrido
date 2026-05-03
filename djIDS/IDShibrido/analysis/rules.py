from django.utils import timezone
from datetime import timedelta
from ..models import Evento

def detect_port_scan(source_ip, window_seconds=60, port_threshold=10):
    now = timezone.now()
    start_time = now - timedelta(seconds=window_seconds)

    eventos = Evento.objects.filter(
        source_ip=source_ip,
        timestamp__gte=start_time
    ).values_list('destination_port', flat=True).distinct()
    print("Puertos únicos:", list(eventos))
    print("Cantidad:", len(eventos))

    return len(eventos) >= port_threshold