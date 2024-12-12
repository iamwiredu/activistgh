from django.db import models

# Create your models here.

class StoreData(models.Model):
    sales  = models.CharField(max_length=255)
    revenue = models.CharField(max_length=255)
    subscribers = models.CharField(max_length=255)