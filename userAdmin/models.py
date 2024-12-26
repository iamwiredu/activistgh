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
