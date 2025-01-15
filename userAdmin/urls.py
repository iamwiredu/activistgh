from django.urls import path
from .views import userAdmin, MessagesReceived, loginPage,deleteRelatedImages,managementDb, Notifications_view,send_emails,productManagement,product_order_view ,OrderDetailsView,send_newsletter_batch,ordersList,distribuition, productEdit

urlpatterns = [
    path('userAdmin/',userAdmin,name='userAdmin'),
        # site management links
    path('managementDb/',managementDb,name='managementDb'),
    path('infodistribuition/',distribuition,name="distribuition"),
    path('productManagement/',productManagement,name='productManagement'),
    path('productEdit/<str:unique_id>/',productEdit,name='productEdit'),
    path('ordersList/',ordersList,name='ordersList'),
    path('send-newsletter-batch/<int:batch_index>/', send_newsletter_batch, name='send_newsletter_batch'),
    path('send_emails/',send_emails,name="sendEmails"),
    path('notifications',Notifications_view.as_view(),name="notifications"),
    path('orderDetails/<str:unique_id>/',OrderDetailsView,name='orderDetails'),
    path('messagesReceived/',MessagesReceived.as_view(),name='messagesReceived'),
    path('product_order/',product_order_view,name='product_order'),
    path('relatedImages/<int:id>/<str:unique_id>/',deleteRelatedImages,name='deleteRelatedImages'),
    path('login/admin',loginPage,name='loginPage')
    ]