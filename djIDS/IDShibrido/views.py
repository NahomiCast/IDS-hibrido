from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.utils import timezone
from .models import Evento, Alerta, RuleConfig
from .analysis.engine import analyze_event

@csrf_exempt
def ingest_evento(request):

    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    data = json.loads(request.body)

    evento = Evento.objects.create(
    
        timestamp=timezone.now(),
        source_ip=data['source_ip'],
        destination_port=data['destination_port'],
        protocol=data['protocol'],
        action=data['action']
    )

    alerts = analyze_event(evento)
    alerts = analyze_event(evento)

    print("ALERTS RETURNED:", alerts)

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


# =========================
# DASHBOARD
# =========================

def dashboard(request):

    eventos = Evento.objects.order_by('-timestamp')[:10]
    alertas = Alerta.objects.order_by('-timestamp')[:10]

    total_eventos = Evento.objects.count()
    total_alertas = Alerta.objects.count()

    port_scans = Alerta.objects.filter(
        alert_type='PORT_SCAN'
    ).count()

    brute_force = Alerta.objects.filter(
        alert_type='BRUTE_FORCE'
    ).count()

    # ========= DONA / RIESGO =========

    critical_count = Alerta.objects.filter(
        severity='critical'
    ).count()

    high_count = Alerta.objects.filter(
        severity='high'
    ).count()

    medium_count = Alerta.objects.filter(
        severity='medium'
    ).count()

    low_count = Alerta.objects.filter(
        severity='low'
    ).count()

    risk_score = (
        critical_count * 40 +
        high_count * 25 +
        medium_count * 15 +
        low_count * 5
    )

    risk_score = min(risk_score, 100)
    safe_score = 100 - risk_score

    # ================================

    context = {
        'eventos': eventos,
        'alertas': alertas,

        'total_eventos': total_eventos,
        'total_alertas': total_alertas,

        'port_scans': port_scans,
        'brute_force': brute_force,

        'risk_score': risk_score,
        'safe_score': safe_score,
        'critical_count': critical_count,
        'high_count': high_count,
        'medium_count': medium_count,
        'low_count': low_count,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


# =========================
# ALERTS VIEW
# =========================

#def alerts_view(request):

    #alertas = Alerta.objects.order_by('-timestamp')

    #return render(request, 'alerts.html', {
   #     'alertas': alertas
  #  })
def alerts_view(request):

    alertas = Alerta.objects.all().order_by('-timestamp')

    return render(request, 'alerts.html', {
        'alertas': alertas
    })

# =========================
# EVENTS VIEW
# =========================

def events_view(request):

    eventos = Evento.objects.all().order_by('-timestamp')
   # return HttpResponse("EVENTS VIEW FUNCIONA")

    return render(request, 'events.html', {
        'eventos': eventos
    })
#=========================
#Rules
#=======================
def rules_view(request):

    rules = RuleConfig.objects.all()

    if request.method == 'POST':

        for rule in rules:

            new_value = request.POST.get(rule.key)

            if new_value:
                rule.value = int(new_value)
                rule.save()

        return redirect('/api/rules/')

    return render(request, 'rules.html', {
        'rules': rules
    })
