# Generated by Django 4.2 on 2024-06-04 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitemmodel',
            old_name='product',
            new_name='service',
        ),
    ]
