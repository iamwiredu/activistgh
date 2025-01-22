import uuid
import requests
from django.db import models
from django.db.models import Case, When, IntegerField  
from userAdmin.models import Notification


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    


class SizeSet(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.name
   
class Size(models.Model):
    size = models.CharField(max_length=255)
    value = models.CharField(max_length=255,null=True,blank=True)
    sizeSet = models.ForeignKey(SizeSet,on_delete=models.SET_NULL,null=True,blank=True, related_name='sizes')
    size_ordering = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['size_ordering']  
        
    def __str__(self):
        return f'{self.size}'

class Product(models.Model):   
    name = models.CharField(max_length=255)
    unique_id = models.UUIDField(editable=False,unique=True,default=uuid.uuid4)
    image = models.ImageField(upload_to='productImages/',null=True,blank=True)
    product_category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    color_tag = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    product_ordering = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    is_active = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    size_set = models.ForeignKey(SizeSet,on_delete=models.CASCADE,null=True,blank=True)
    size_av = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['product_ordering'] 
    
    def __str__(self):
        color_tag = self.color_tag
        if color_tag:
            return f'{self.name}  {color_tag} Category:{self.product_category}' 
        else:
            return f'{self.name}  {color_tag} Category:{self.product_category}' 
            color_tag = ''
    
    @property
    def stock_actual(self):
        if self.size_set:
            if self.size_set.name == '39 - 46':
                return self.size39to46.size39 + self.size39to46.size40 + self.size39to46.size41 + self.size39to46.size42 + self.size39to46.size43 + self.size39to46.size44 + self.size39to46.size45 + self.size39to46.size46
            elif self.size_set.name == 'Medium Large Xl 2xl 3xl':
                return self.mediumLargeStock.medium + self.mediumLargeStock.large + self.mediumLargeStock.xl + self.mediumLargeStock.xl2 + self.mediumLargeStock.xl3
        else:
            return self.stock
    
    def get_size(self,size):
        get = getattr(self.size_set,size,0)
        if get:
            return get
        else:
            return 0
        

class MediumLargeStock(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='mediumLargeStock')
    size_set = models.ForeignKey(SizeSet,on_delete=models.CASCADE,null=True,blank=True)
    medium = models.PositiveIntegerField(default=0)
    large = models.PositiveIntegerField(default=0)
    xl = models.PositiveIntegerField(default=0)
    xl2 = models.PositiveIntegerField(default=0)
    xl3 = models.PositiveIntegerField(default=0)

class Size39to46(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='size39to46')
    size_set = models.ForeignKey(SizeSet,on_delete=models.CASCADE,null=True,blank=True)
    size39 = models.PositiveIntegerField(default=0)
    size40 = models.PositiveIntegerField(default=0)
    size41 = models.PositiveIntegerField(default=0)
    size42 = models.PositiveIntegerField(default=0)
    size43 = models.PositiveIntegerField(default=0)
    size44 = models.PositiveIntegerField(default=0)
    size45 = models.PositiveIntegerField(default=0)
    size46 = models.PositiveIntegerField(default=0)


class RelatedImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='relatedImages')
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
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Call the parent save method to save the instance
        super().save(*args, **kwargs)

        # API endpoint and payload
        endPoint = "https://api.mnotify.com/api/contact"
        # apiKey = 'g8s7yo7Mxf88LFw1SCHKBoQZf'
        # groupId = 54135
        apiKey = '4Vrc1NP8PUeS4nB51QgHvkD4W'
        groupId = 54118
        data = {
            'phone': str(self.phone),
            'title':'None',
            'firstname': str(self.first_name),
            'lastname': str(self.last_name),
            'email': self.email,
            'dob': '2003-05-05',
        }
        print(self.phone,self.email)
        url = endPoint + '/' + str(groupId) + '?key=' + apiKey
        # Make the API request
        response = requests.post(url, data)
        print(response.json())

class Payment(models.Model):
    # personal details 
    unique_id = models.UUIDField(unique=True,editable=False,default=uuid.uuid4)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    country_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,blank=True)
    email = models.EmailField(blank=True)
    order_notes = models.TextField(blank=True)

    # delivery Address
    street_address_1 = models.CharField(max_length=255, verbose_name='Street Address Line 1', null=True)
    street_address_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Street Address Line 2 (optional)')
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    destination_country = models.CharField(max_length=100, null=True)
    accralocation = models.CharField(max_length=255,null=True,blank=True)
    

    additional_info = models.TextField(blank=True)

    # cart and payment
    amount = models.PositiveIntegerField(blank=True)
    ref = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
   
    verified = models.BooleanField(default=False)
    delivery_price = models.IntegerField(default=0)
    delivered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    pickupdata = models.BooleanField(default=False)
    

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return f'Payment: {self.amount}'

    @property
    def get_formatted_address(self):
        """
        Returns a nicely formatted delivery address for display purposes.
        """
        address_lines = [
            self.street_address_1,
            self.street_address_2,
            f"{self.city}, {self.state} {self.zip_code}" if self.state else f"{self.city} {self.zip_code}",
            self.destination_country,
        ]
        # Filter out empty or None lines
        return "<br>".join(filter(None, address_lines))

    
    @property
    def amount_value(self) -> int:
        self.amount * 100
        return self.amount*100
    
    @property
    def delivery_actual(self) -> int:
        return self.delivery_price * 16
    
    @property
    def total_actual(self) -> int:
        return self.amount + (self.delivery_price * 16)
    
    @property
    def order_id(self):
        val = str(self.id)
        if len(val) >= 4: # more than 4 values
            return 'PO-' + val
        else:
            loopCount = 4 - len(val)
            for i in range(loopCount):
                val = '0'+ val
            return 'PO-'+ val



class Cart(models.Model):
    payment = models.OneToOneField(Payment,on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)


class CartObject(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_objects')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    size = models.CharField(max_length=255)
    sizeData = models.CharField(max_length=255,null=True,blank=True)
    quantity = models.IntegerField()

    @property
    def price(self):
        return self.quantity * self.product.price
    
   
class NewsletterBatch(models.Model):
    batch = models.TextField(null=True,blank=True)
    batch_size = models.CharField(max_length=255,null=True,blank=True)

class UserLogin(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField()
    notification = models.OneToOneField(Notification,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.first_name}"
    
