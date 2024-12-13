from django.urls import path
from .views import userAdmin, managementDb, productManagement, ordersList,distribuition, productEdit

urlpatterns = [
    path('userAdmin/',userAdmin,name='userAdmin'),
        # site management links
    path('managementDb/',managementDb,name='managementDb'),
    path('infodistribuition/',distribuition,name="distribuition"),
    path('productManagement/',productManagement,name='productManagement'),
    path('productEdit/<str:unique_id>/',productEdit,name='productEdit'),
    path('ordersList/',ordersList,name='ordersList')
]