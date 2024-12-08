from django.urls import path
from .views import userAdmin

urlpatterns = [
    path('userAdmin/',userAdmin,name='userAdmin')
]