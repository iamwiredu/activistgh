import uuid
from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    unique_id = models.UUIDField(editable=False,unique=True,default=uuid.uuid4)
    image = models.ImageField(upload_to='strangers/productImages/',null=True,blank=True)
    category = models.CharField(max_length=255,null=True,blank=True)
    color_tag = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    product_ordering = models.PositiveIntegerField(null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    stock = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    is_active = models.BooleanField(default=True)
    size_av = models.BooleanField(default=True)
    
    def __str__(self):
        color_tag = self.color_tag
        if color_tag:
            return f'{self.name}  {color_tag} Category:{self.category}' 
        else:
            color_tag = ''
            return f'{self.name}  {color_tag} Category:{self.category}' 
        
            
