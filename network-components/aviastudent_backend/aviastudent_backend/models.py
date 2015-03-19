from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


class Vehicle(models.Model):

    user = models.OneToOneField(User, verbose_name='Vehicle account')
    description = models.TextField(verbose_name='Vehicle description')

    def __str__(self):
        return 'Vehicle %s, "%s"' % (self.id, self.description)


class Telemetry(models.Model):

    vehicle = models.ForeignKey(Vehicle, verbose_name='Source vehicle')
    record = JSONField(verbose_name='Telemetry data')

    def __str__(self):
        return 'Telemetry entry of vehicle "%s", ' % (self.vehicle.id, self.vehicle.description)


class OnlineSubscription(models.Model):

    user = models.ForeignKey(User, verbose_name='Subscriber')
    vehicle = models.OneToOneField(Vehicle, verbose_name='Target vehicle')

    def __str__(self):
        return 'Subscription of user %s to vehicle "%s"' % (self.user.username, self.vehicle.description)
