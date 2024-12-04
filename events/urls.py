from django.urls import path
from .views import events


urlpatterns = [
    path('event/<str:unique_id>/',events,name='event')
]