from django.urls import path
from .views import shop, productDetail, checkout, makePayment, orderSuccess, orderDetails

urlpatterns =[
    path('shop/',shop,name='shop'),
    path('productDetail/<str:unique_id>/',productDetail,name='productDetail'),
    path('checkout',checkout,name='checkout'),
    path('makePayment/<str:ref>/',makePayment,name='makePayment'),
    path('orderSuccess/<str:ref>/',orderSuccess,name='orderSuccess'),
    path('orderDetails/<str:ref>/',orderDetails,name='orderDetails')
]