from django.contrib import admin
from .models import Product, Cart, CartObject,RelatedImages



admin.site.register(Product)
admin.site.register(RelatedImages)
admin.site.register(Cart)
admin.site.register(CartObject)