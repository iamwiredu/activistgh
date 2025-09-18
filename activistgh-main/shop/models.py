import uuid
from django.db import models
from payment.models import Payment

# Create your models here.

class Product(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField(blank=True,default=name)
    details = models.TextField(blank=True,default=name)
    image = models.ImageField(upload_to='productImages/')
    order_number = models.PositiveIntegerField(null=True,blank=True)
    tag = models.CharField(max_length=255,null=True,blank=True)
    hasSize = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class RelatedImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='relatedImages/')



class Cart(models.Model):
    payment = models.OneToOneField(Payment,on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)


class CartObject(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_objects')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    size = models.CharField(max_length=255)
    quantity = models.IntegerField()

    @property
    def price(self):
        return self.quantity * self.product.price
    
