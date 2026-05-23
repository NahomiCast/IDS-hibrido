from scapy.all import sniff, IP, TCP

import os
import django

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'djIDS.settings'
)

django.setup()

from IDShibrido.models import Evento
from IDShibrido.analysis.engine import analyze_event
from IDShibrido.models import Alerta

from django.utils import timezone


def process_packet(packet):
    print(packet.summary())

    if packet.haslayer(IP) and packet.haslayer(TCP):

        source_ip = packet[IP].src
        destination_port = packet[TCP].dport

        # SOLO tráfico desde Kali
      
        

        print(f"[+] {source_ip}:{destination_port}")

        evento = Evento.objects.create(
            timestamp=timezone.now(),
            source_ip=source_ip,
            destination_port=destination_port,
            protocol='TCP',
            action='network_traffic'
        )

        alerts = analyze_event(evento)

        for alert in alerts:

            Alerta.objects.create(
                source_ip=alert['source_ip'],
                alert_type=alert['type'],
                severity=alert['severity']
            )

            print("[ALERT]", alert)


print("[*] Starting packet capture...")

sniff(
    iface="Wi-Fi",
    filter="tcp",
    prn=process_packet,
    store=False
)
#====================================
