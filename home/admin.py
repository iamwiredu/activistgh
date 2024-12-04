from django.contrib import admin
from .models import Product, Outing, TicketType

# Register your models here.

admin.site.register(Product)
admin.site.register(Outing)
admin.site.register(TicketType)