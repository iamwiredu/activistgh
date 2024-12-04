import uuid
from django.db import models

# Assuming the EventModel is defined as before
class EventModel(models.Model):
    # Core Attributes
    unique_id = models.UUIDField(default=uuid.uuid4,unique=True,null=True,editable=False)
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


# Second model for TicketType, inheriting from EventModel
class TicketType(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False,null=True)
    events = models.ForeignKey(EventModel,on_delete=models.CASCADE,null=True,blank=True)
    ticket_type_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.PositiveIntegerField(default=0)
    sold_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.ticket_type_name} for {self.name}"

    class Meta:
        verbose_name = "Ticket Type"
        verbose_name_plural = "Ticket Types"
