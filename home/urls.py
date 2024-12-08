from django.urls import path
from .views import home, productDetailPage, shop, managementDb, productManagement

urlpatterns = [
    path('',home,name='home'),
    path('product/<str:unique_id>/',productDetailPage,name='productDetailPage'),
    path('shop/',shop,name="shop"),


    # site management links
    path('managementDb/',managementDb,name='managementDb'),
    path('managementDb/productMangement',productManagement,name="productManagement")
]