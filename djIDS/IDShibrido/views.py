from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import datetime

from .models import Evento, Alerta
from .analysis.engine import analyze_event


@csrf_exempt
def ingest_evento(request):

    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    data = json.loads(request.body)

    evento = Evento.objects.create(
        timestamp=datetime.fromisoformat(data['timestamp']),
        source_ip=data['source_ip'],
        destination_port=data['destination_port'],
        protocol=data['protocol'],
        action=data['action']
    )

    alerts = analyze_event(evento)

    for alert in alerts:
        Alerta.objects.create(
            source_ip=alert['source_ip'],
            alert_type=alert['type'],
            severity=alert['severity']
        )

    return JsonResponse({
        'status': 'ok',
        'id': evento.id,
        'alerts': alerts
    })


def dashboard(request):

    eventos = Evento.objects.order_by('-timestamp')[:20]
    alertas = Alerta.objects.order_by('-timestamp')[:20]

    context = {
        'eventos': eventos,
        'alertas': alertas
    }

    return render(request, 'dashboard.html', context)