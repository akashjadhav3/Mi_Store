# Generated by Django 3.0.8 on 2021-06-06 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20210516_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='login',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=70)),
            ],
        ),
    ]
