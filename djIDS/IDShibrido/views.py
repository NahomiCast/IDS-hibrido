from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import Evento

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

    return JsonResponse({'status': 'ok', 'id': evento.id})