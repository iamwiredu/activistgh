import uuid
from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    unique_id = models.UUIDField(editable=False,unique=True,default=uuid.uuid4)
    image = models.ImageField(upload_to='productImages/',null=True,blank=True)
    category = models.CharField(max_length=255,null=True,blank=True)
    color_tag = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    product_ordering = models.PositiveIntegerField(null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    stock = models.CharField(null=True,blank=True,default=0)
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

class RelatedImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='strangers/relatedImages',null=True,blank=True)
    
    def __str__(self):
        return f'{self.product}'
    
# Assuming the EventModel is defined as before
class Outing(models.Model):
    # Core Attributes
   
    unique_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # Date and Time
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    # Location
    location_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Ticketing
    capacity = models.PositiveIntegerField(default=0)  # 0 for unlimited capacity
    tickets_sold = models.PositiveIntegerField(default=0)

    # Media
    cover_image = models.ImageField(upload_to='strangers/events',null=True,blank=True)  # New attribute for the cover image
    gallery = models.JSONField(blank=True, null=True)  # List of image/video URLs

    organizer_contact = models.EmailField(blank=True, null=True)

    # Engagement
    rsvp_count = models.PositiveIntegerField(default=0)

    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_datetime']
        verbose_name = "Event"
        verbose_name_plural = "Events"


class TicketType(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    events = models.ForeignKey(Outing,on_delete=models.CASCADE,null=True,blank=True)
    ticket_type_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.PositiveIntegerField(default=0)
    sold_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.ticket_type_name} for {self.name}"

    class Meta:
        verbose_name = "Ticket Type"
        verbose_name_plural = "Ticket Types"
    

class Newsletter(models.Model):
    email = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
