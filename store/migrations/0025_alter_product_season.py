# Generated by Django 5.0 on 2023-12-12 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_delete_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='season',
            field=models.CharField(choices=[('2023-24', '2023-24'), ('2023', '2023'), ('2022-23', '2022-23'), ('2022', '2022'), ('2021-22', '2021-22'), ('2021', '2021'), ('2020-21', '2020-21'), ('2020', '2020'), ('2019-20', '2019-20'), ('2019', '2019'), ('2018-19', '2018-19'), ('2018', '2018'), ('2017-18', '2017-18'), ('2017', '2017'), ('2016-17', '2016-17'), ('2016', '2016'), ('2015-16', '2015-16'), ('2015', '2015'), ('2014-15', '2014-15'), ('2014', '2014'), ('2013-14', '2013-14'), ('2013', '2013'), ('2012-13', '2012-13'), ('2012', '2012'), ('2011-12', '2011-12'), ('2011', '2011'), ('2010-11', '2010-11'), ('2010', '2010'), ('2008-09', '2008-09')], max_length=100),
        ),
    ]
