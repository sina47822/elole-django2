# Generated by Django 4.2 on 2024-09-26 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stylist', '0005_remove_stylist_services_remove_workday_specifictime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecificWorkHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_hour', models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)], null=True)),
                ('to_hour', models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)], null=True)),
                ('add_remove', models.BooleanField(default=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='workday',
            name='general_hours',
        ),
        migrations.RemoveField(
            model_name='workday',
            name='stylist',
        ),
        migrations.AddField(
            model_name='portfolioimage',
            name='word_day',
            field=models.ManyToManyField(blank=True, to='stylist.workday'),
        ),
        migrations.AddField(
            model_name='portfolioimage',
            name='word_hour',
            field=models.ManyToManyField(blank=True, to='stylist.workhour'),
        ),
        migrations.AddField(
            model_name='portfolioimage',
            name='special_work_times',
            field=models.ManyToManyField(blank=True, to='stylist.specificworkhour'),
        ),
    ]
