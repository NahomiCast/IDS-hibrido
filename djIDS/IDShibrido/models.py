from django.db import models

class Evento(models.Model):
    timestamp = models.DateTimeField()
    source_ip = models.GenericIPAddressField()
    destination_port = models.IntegerField()
    protocol = models.CharField(max_length=10)
    action = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.source_ip}:{self.destination_port} - {self.action}"
