# Generated by Django 4.1.3 on 2023-10-26 23:54

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_product_extra_photos2_product_extra_photos3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='league',
            field=models.CharField(choices=[('Bundesliga', 'Bundesliga'), ('Champions League', 'Champions League'), ('Europa League', 'Europa League'), ('La Liga', 'La Liga'), ('Ligue 1', 'Ligue 1'), ('Premier League', 'Premier League'), ('Serie A', 'Serie A'), ('World Cup', 'World Cup'), ('Worldwide Jerseys', 'Worldwide Jerseys'), ('B-Jerseys Specials', 'B-Jerseys Specials'), ('Special Edition', 'Special Edition')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='extra_photos2',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to=store.models.upload_extra_photos2),
        ),
        migrations.AlterField(
            model_name='product',
            name='extra_photos3',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to=store.models.upload_extra_photos3),
        ),
        migrations.AlterField(
            model_name='product',
            name='extra_photos4',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to=store.models.upload_extra_photos4),
        ),
    ]
