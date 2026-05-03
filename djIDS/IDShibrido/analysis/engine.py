from .rules import detect_port_scan

def analyze_event(evento):
    alerts = []

    if detect_port_scan(evento.source_ip):
        alerts.append({
            'type': 'PORT_SCAN',
            'source_ip': evento.source_ip,
            'severity': 'high'
        })

    return alerts