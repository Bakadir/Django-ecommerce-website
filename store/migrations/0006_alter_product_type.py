# Generated by Django 4.1.3 on 2023-10-19 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_club_league_alter_product_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('home', 'home'), ('away', 'away'), ('third', 'third')], max_length=10),
        ),
    ]
