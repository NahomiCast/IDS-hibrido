from django.utils import timezone
from datetime import timedelta

from ..models import Evento
from ..models import RuleConfig


# =========================
# PORT SCAN
# =========================

def detect_port_scan(source_ip, window_seconds=60):

    threshold = int(
        RuleConfig.objects.get(
            key='PORT_SCAN_THRESHOLD'
        ).value
    )

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
    print("Threshold:", threshold)

    return count >= threshold


# =========================
# BRUTE FORCE
# =========================

def detect_brute_force(source_ip, window_seconds=60):

    threshold = int(
        RuleConfig.objects.get(
            key='BRUTE_FORCE_THRESHOLD'
        ).value
    )

    now = timezone.now()

    start_time = now - timedelta(seconds=window_seconds)

    intentos = Evento.objects.filter(
        source_ip=source_ip,
        timestamp__gte=start_time,
        action='login_failed'
    )

    count = intentos.count()

    print("Intentos fallidos:", count)
    print("Threshold:", threshold)

    return count >= threshold