from django.urls import path
from .views import home, gallery, adminLogin, orderList


urlpatterns = [
    path('',home,name='homePage'),
    path('gallery/',gallery,name='gallery'),
    path('orders/',adminLogin,name='adminLogin'), #set login of admin to orders
    path('orders/list/',orderList,name='orderList')
]