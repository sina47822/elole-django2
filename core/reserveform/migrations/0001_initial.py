# Generated by Django 4.2 on 2024-09-25 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stylist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveForm_Paid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReserveForm_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReserveFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserveform', to=settings.AUTH_USER_MODEL)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stylist.workday')),
                ('hour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stylist.workhour')),
                ('paid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reserveform.reserveform_paid')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stylist.services')),
                ('service_category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='stylist.servicecategorymodel')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reserveform.reserveform_status')),
                ('stylist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserveform', to='stylist.stylist')),
            ],
        ),
    ]
