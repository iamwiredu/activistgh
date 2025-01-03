from django.contrib import admin
from .models import Product, Outing, Payment,TicketType, RelatedImages, Newsletter, UserLogin, Contact

# Register your models here.

admin.site.register(Product)
admin.site.register(Outing)
admin.site.register(TicketType)
admin.site.register(RelatedImages)
admin.site.register(Newsletter)
admin.site.register(UserLogin)
admin.site.register(Contact)
admin.site.register(Payment)