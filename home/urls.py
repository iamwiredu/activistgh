from django.urls import path
from .views import home,productDetailPage, get_stock,shop, checkout, contactPage, makePayment, orderSuccess
urlpatterns = [
    path('',home,name='home'),
    path('product/<str:unique_id>/',productDetailPage,name='productDetailPage'),
    path('shop/<str:category_name>/',shop,name="shop"),
    path('checkout/',checkout,name='checkout'),
    path('contactPage/',contactPage,name="contact"),
    path('makePayment/<str:ref>/',makePayment,name='makePayment'),
    path('orderSuccess/<str:ref>/',orderSuccess,name='orderSuccess'),
    path('get-stock/', get_stock, name='get_stock'),
]
