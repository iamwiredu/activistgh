from django.urls import path
from .views import home,productDetailPage, shop, checkout, contactPage, makePayment, orderSuccess
urlpatterns = [
    path('',home,name='home'),
    path('product/<str:unique_id>/',productDetailPage,name='productDetailPage'),
    path('shop/',shop,name="shop"),
    path('checkout/',checkout,name='checkout'),
    path('contactPage/',contactPage,name="contact"),
    path('makePayment/<str:ref>/',makePayment,name='makePayment'),
    path('orderSuccess/<str:ref>/',orderSuccess,name='orderSuccess'),

]