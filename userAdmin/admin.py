from django.contrib import admin
from .models import Revenue, Notification, DeliveryPriceByRegion

admin.site.register(Revenue)
admin.site.register(Notification)
admin.site.register(DeliveryPriceByRegion)