# Generated by Django 5.0.6 on 2025-04-18 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_product_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hasSize',
            field=models.BooleanField(default=True),
        ),
    ]
