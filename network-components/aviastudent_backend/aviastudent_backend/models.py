from django.db import models
from django.contrib.auth.models import User
from django_pgjson.fields import JsonBField


class Vehicle(models.Model):

    user = models.OneToOneField(User, verbose_name='Vehicle account')
    description = models.TextField(verbose_name='Vehicle description')
    subscribed_to = models.ManyToManyField(User, verbose_name='Accounts subscribed to', related_name='subscribed_vehicles')

    def __str__(self):
        return 'Vehicle %s, "%s"' % (self.id, self.description)


class Telemetry(models.Model):

    vehicle = models.ForeignKey(Vehicle, verbose_name='Source vehicle')
    record = JsonBField(verbose_name='Telemetry data')
    timestamp = models.DateTimeField(verbose_name='Mobile terminal timestamp')

    def __str__(self):
        return 'Telemetry entry of vehicle "%s", %s' % (self.vehicle.description, self.timestamp)
