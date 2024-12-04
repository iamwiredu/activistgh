from django.db import models

# Create your models here.

from django.db import models
from django.utils.timezone import now

class EventModel(models.Model):
    # Core Attributes
    id = models.UUIDField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # Date and Time
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    # Location
    location_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Ticketing
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Free if 0
    capacity = models.PositiveIntegerField(default=0)  # 0 for unlimited capacity
    tickets_sold = models.PositiveIntegerField(default=0)

    # Media
    cover_image = models.URLField(blank=True, null=True)  # New attribute for the cover image
    event_image = models.URLField(blank=True, null=True)
    gallery = models.JSONField(blank=True, null=True)  # List of image/video URLs

    # Organizer
    organizer_name = models.CharField(max_length=255)
    organizer_contact = models.EmailField(blank=True, null=True)

    # Engagement
    rsvp_count = models.PositiveIntegerField(default=0)
    social_links = models.JSONField(blank=True, null=True)  # List of URLs

    # Advanced Features
    recurring = models.BooleanField(default=False)
    tags = models.JSONField(blank=True, null=True)  # List of tags
    status = models.CharField(max_length=50, choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('canceled', 'Canceled'),
    ], default='draft')

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
