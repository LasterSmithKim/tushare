# Generated by Django 2.2.4 on 2019-08-04 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_stock_all_stock_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock_all',
            name='open',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
            preserve_default=False,
        ),
    ]
