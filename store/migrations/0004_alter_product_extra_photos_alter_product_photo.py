# Generated by Django 4.1.3 on 2023-10-17 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_clubs_club_rename_products_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='extra_photos',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to=''),
        ),
    ]