# Generated by Django 3.0.8 on 2021-06-07 03:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_signin'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='password',
            field=models.CharField(default=django.utils.timezone.now, max_length=70),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='signin',
            name='password',
            field=models.CharField(default='', max_length=70),
        ),
    ]
