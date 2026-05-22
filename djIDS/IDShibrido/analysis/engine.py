
from .rules import detect_port_scan, detect_brute_force


def analyze_event(evento):

    alerts = []

    # PORT SCAN
    if detect_port_scan(evento.source_ip):

        alerts.append({
            'type': 'PORT_SCAN',
            'source_ip': evento.source_ip,
            'severity': 'high'
        })

    # BRUTE FORCE
    if detect_brute_force(evento.source_ip):

        alerts.append({
            'type': 'BRUTE_FORCE',
            'source_ip': evento.source_ip,
            'severity': 'critical'
        })

    return alerts