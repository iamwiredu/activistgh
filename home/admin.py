from django.contrib import admin
from .models import Product, Outing, TicketType, RelatedImages

# Register your models here.

admin.site.register(Product)
admin.site.register(Outing)
admin.site.register(TicketType)
admin.site.register(RelatedImages)