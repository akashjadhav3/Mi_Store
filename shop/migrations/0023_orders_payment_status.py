# Generated by Django 2.1.5 on 2021-07-05 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_orders_order_id2'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]