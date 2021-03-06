# Generated by Django 2.1.5 on 2021-07-31 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_orders_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orders',
            options={'verbose_name': 'Orders', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='payments',
            options={'verbose_name': 'payment', 'verbose_name_plural': 'payment'},
        ),
        migrations.AlterField(
            model_name='product',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
