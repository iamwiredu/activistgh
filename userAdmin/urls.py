from django.urls import path
from .views import userAdmin, managementDb, send_emails,productManagement, send_newsletter_batch,ordersList,distribuition, productEdit

urlpatterns = [
    path('userAdmin/',userAdmin,name='userAdmin'),
        # site management links
    path('managementDb/',managementDb,name='managementDb'),
    path('infodistribuition/',distribuition,name="distribuition"),
    path('productManagement/',productManagement,name='productManagement'),
    path('productEdit/<str:unique_id>/',productEdit,name='productEdit'),
    path('ordersList/',ordersList,name='ordersList'),
    path('send-newsletter-batch/<int:batch_index>/', send_newsletter_batch, name='send_newsletter_batch'),
    path('send_emails/',send_emails,name="sendEmails")
]