# Generated by Django 4.1.3 on 2023-10-19 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_club_league'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='favorite_in_league',
        ),
    ]
