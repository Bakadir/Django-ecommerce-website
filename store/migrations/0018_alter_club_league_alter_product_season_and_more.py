# Generated by Django 4.1.3 on 2023-10-26 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_club_league_alter_product_extra_photos2_and_more'),
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
            field=models.CharField(choices=[('2023-24', '2023-24'), ('2023', '2023'), ('2022-23', '2022-23'), ('2022', '2022'), ('2021-22', '2021-22'), ('2021', '2021'), ('2020-21', '2020-21'), ('2020', '2020'), ('2019-20', '2019-20'), ('2019', '2019'), ('2018-19', '2018-19'), ('2018', '2018'), ('2017-18', '2017-18'), ('2017', '2017'), ('2016-17', '2016-17'), ('2016', '2016'), ('2015-16', '2015-16'), ('2015', '2015'), ('2014-15', '2014-15'), ('2014', '2014'), ('2013-14', '2013-14'), ('2013', '2013'), ('2012-13', '2012-13'), ('2012', '2012'), ('2011-12', '2011-12'), ('2011', '2011'), ('2010-11', '2010-11'), ('2010', '2010')], max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('home', 'home'), ('away', 'away'), ('third', 'third'), ('Special Edition', 'Special Edition')], max_length=100),
        ),
    ]
