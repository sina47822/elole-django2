# Generated by Django 4.2 on 2024-09-25 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stylist', '0004_alter_workday_stylist_alter_workhour_workday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stylist',
            name='services',
        ),
        migrations.RemoveField(
            model_name='workday',
            name='specifictime',
        ),
        migrations.DeleteModel(
            name='SpecificWorkHour',
        ),
    ]
