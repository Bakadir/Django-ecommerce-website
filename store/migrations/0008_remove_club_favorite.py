# Generated by Django 4.1.3 on 2023-10-19 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_club_favorite_in_league'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='favorite',
        ),
    ]