# Generated by Django 5.0.6 on 2024-10-24 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_product_description_alter_product_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default=models.CharField(max_length=255)),
        ),
        migrations.AlterField(
            model_name='product',
            name='details',
            field=models.TextField(blank=True, default=models.CharField(max_length=255)),
        ),
    ]
