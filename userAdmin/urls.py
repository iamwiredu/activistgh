from django.urls import path
from .views import userAdmin, managementDb, productManagement, distribuition

urlpatterns = [
    path('userAdmin/',userAdmin,name='userAdmin'),
        # site management links
    path('managementDb/',managementDb,name='managementDb'),
    path('infodistribuition/',distribuition,name="distribuition"),
    path('productManagement/',productManagement,name='productManagement')
]