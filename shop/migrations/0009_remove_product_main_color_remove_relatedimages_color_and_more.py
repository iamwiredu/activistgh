# Generated by Django 5.0.6 on 2024-10-23 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_product_main_color_alter_relatedimages_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='main_color',
        ),
        migrations.RemoveField(
            model_name='relatedimages',
            name='color',
        ),
        migrations.DeleteModel(
            name='Color',
        ),
    ]
