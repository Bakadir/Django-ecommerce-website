# Generated by Django 4.1.3 on 2023-10-16 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_product_products'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Clubs',
            new_name='Club',
        ),
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]