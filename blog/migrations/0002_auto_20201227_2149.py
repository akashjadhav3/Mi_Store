# Generated by Django 3.0.8 on 2020-12-27 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='tilte',
            new_name='title',
        ),
    ]