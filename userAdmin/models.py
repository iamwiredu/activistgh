from django.db import models

# Create your models here.

class Revenue(models.Model):
    year = models.PositiveIntegerField(unique=True)  # One record per year
    january = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    february = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    march = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    april = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    may = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    june = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    july = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    august = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    september = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    october = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    november = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    december = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Revenue for {self.year}"

    def update_monthly_revenue(self, month, amount):
        """Update the revenue for a specific month."""
        # Map month numbers to field names
        month_field_mapping = {
            1: 'january', 2: 'february', 3: 'march', 4: 'april',
            5: 'may', 6: 'june', 7: 'july', 8: 'august',
            9: 'september', 10: 'october', 11: 'november', 12: 'december'
        }

        field_name = month_field_mapping.get(month)
        if field_name:
            current_revenue = getattr(self, field_name)
            setattr(self, field_name, current_revenue + amount)
            self.save()

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        productSold = 'Product Sold'
        newsLetterAddition = 'NewsLetter Addition'
        contactForm = 'Contact Form'

    title = models.CharField(max_length=100)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    notification_type= models.CharField(max_length=100, choices=NotificationType.choices, null=True,blank=True)
    viewed = models.BooleanField(default=False)
    def __str__(self):
        return self.title


from django.db import models

class DeliveryPriceByRegion(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    delivery_method = models.CharField(max_length=100, unique=True)  # Delivery method name (e.g., "Standard", "Express")
    ashanti = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    greater_accra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    volta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    western = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eastern = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    northern = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upper_east = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upper_west = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bono = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bono_east = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ahafo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savannah = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    western_north = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    oti = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    central = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery Method: {self.delivery_method}"
