from .rules import detect_port_scan, detect_brute_force
from IDShibrido.models import Alerta

def analyze_event(evento):

    alerts = []

    print(f"Analizando: {evento.source_ip}")

    # =========================
    # PORT SCAN
    # =========================

    port_scan_detected = detect_port_scan(
        evento.source_ip
    )

    print("Port scan:", port_scan_detected)

    if port_scan_detected:

        alerts.append({
            'type': 'PORT_SCAN',
            'source_ip': evento.source_ip,
            'severity': 'high'
        })

    # =========================
    # BRUTE FORCE
    # =========================

    brute_force_detected = detect_brute_force(
        evento.source_ip
    )

    print("Brute force:", brute_force_detected)

    if brute_force_detected:

        alerts.append({
            'type': 'BRUTE_FORCE',
            'source_ip': evento.source_ip,
            'severity': 'critical'
        })

    return alerts