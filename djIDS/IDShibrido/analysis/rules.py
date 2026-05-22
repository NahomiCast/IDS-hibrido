from django.utils import timezone
from datetime import timedelta
from ..models import Evento

from ..models import RuleConfig
def detect_port_scan(source_ip, window_seconds=60):

    threshold = RuleConfig.objects.get(
        key='PORT_SCAN_THRESHOLD'
    ).value

    now = timezone.now()

    start_time = now - timedelta(seconds=window_seconds)

    eventos = Evento.objects.filter(
        source_ip=source_ip,
        timestamp__gte=start_time
    ).values_list(
        'destination_port',
        flat=True
    ).distinct()

    count = len(eventos)

    print("Puertos únicos:", list(eventos))
    print("Cantidad:", count)

    # SOLO dispara cuando llega EXACTAMENTE al umbral
    return count == threshold

def detect_brute_force(source_ip, window_seconds=30, attempt_threshold=5):
    now = timezone.now()
    start_time = now - timedelta(seconds=window_seconds)

    eventos = Evento.objects.filter(
        source_ip=source_ip,
        timestamp__gte=start_time,
        action="login_failed"
    )

    count = eventos.count()

    print("Intentos fallidos:", count)

    return count == attempt_threshold