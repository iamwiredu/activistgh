# Generated by Django 5.0.6 on 2024-10-28 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_rename_delviered_payment_delivered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='delivery_address',
        ),
        migrations.AddField(
            model_name='payment',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='destination_country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='street_address_1',
            field=models.CharField(max_length=255, null=True, verbose_name='Street Address Line 1'),
        ),
        migrations.AddField(
            model_name='payment',
            name='street_address_2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Street Address Line 2 (optional)'),
        ),
        migrations.AddField(
            model_name='payment',
            name='zip_code',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='additional_info',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='payment',
            name='first_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='last_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='phone',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
