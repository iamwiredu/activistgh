from django.urls import path
from .views import events


urlpatterns = [
    path('event/',events,name='event')
]