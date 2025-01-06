from django.urls import path
from .views import Events, EventDetailView


urlpatterns = [
    # path('event/<str:unique_id>/',events,name='event'),
    path('events/',Events.as_view(),name='events'),
    path('eventdetail/<str:unique_id>/',EventDetailView.as_view(),name='event')
]