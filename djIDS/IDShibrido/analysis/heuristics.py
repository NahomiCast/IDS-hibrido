from django.utils import timezone
from datetime import timedelta

from ..models import Evento
from ..models import RuleConfig


# =========================
# TRAFFIC ANOMALY
# =========================

def detect_traffic_anomaly(source_ip, window_seconds=60):

    threshold = int(
        RuleConfig.objects.get(
            key='ANOMALY_THRESHOLD'
        ).value
    )

    now = timezone.now()

    start_time = now - timedelta(
        seconds=window_seconds
    )

    eventos = Evento.objects.filter(
        source_ip=source_ip,
        timestamp__gte=start_time
    )

    count = eventos.count()

    print("=== HEURISTIC ANALYSIS ===")
    print("IP:", source_ip)
    print("Eventos recientes:", count)
    print("Threshold:", threshold)

    return count >= threshold