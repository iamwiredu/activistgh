from django.db import models
import uuid

# Create your models here.
class Payment(models.Model):
    # personal details 
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
    

    additional_info = models.TextField(blank=True)

    # cart and payment
    amount = models.PositiveIntegerField(blank=True)
    ref = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
   
    verified = models.BooleanField(default=False)
    delivery_price = models.IntegerField(default=0)
    delivered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return f'Payment: {self.amount}'

    
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

