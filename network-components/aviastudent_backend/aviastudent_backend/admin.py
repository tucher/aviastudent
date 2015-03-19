from django.contrib import admin
from aviastudent_backend.models import Vehicle, Telemetry, OnlineSubscription

admin.site.register(Vehicle)
admin.site.register(Telemetry)
admin.site.register(OnlineSubscription)
