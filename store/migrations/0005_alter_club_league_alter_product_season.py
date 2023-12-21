# Generated by Django 4.1.3 on 2023-10-19 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_extra_photos_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='league',
            field=models.CharField(choices=[('Bundesliga', 'Bundesliga'), ('Champions League', 'Champions League'), ('Europa League', 'Europa League'), ('La Liga', 'La Liga'), ('Ligue 1', 'Ligue 1'), ('Premier League', 'Premier League'), ('Serie A', 'Serie A'), ('World Cup', 'World Cup'), ('Worldwide Jerseys', 'Worldwide Jerseys'), ('B-Jerseys Specials', 'B-Jerseys Specials')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='season',
            field=models.CharField(choices=[('2023/24', '2023/24'), ('2022/23', '2022/23'), ('2022', '2022'), ('2023', '2023')], max_length=10),
        ),
    ]
