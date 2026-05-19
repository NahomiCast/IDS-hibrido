from django.db import models

class Evento(models.Model):
    timestamp = models.DateTimeField()
    source_ip = models.GenericIPAddressField()
    destination_port = models.IntegerField()
    protocol = models.CharField(max_length=10)
    action = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.source_ip}:{self.destination_port} - {self.action}"


class Alerta(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField()
    alert_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.alert_type} - {self.source_ip}"