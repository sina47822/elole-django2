# Generated by Django 4.2 on 2024-06-05 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('email', models.EmailField(help_text='Please provide email in case of cancellation.', max_length=254)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('question1', models.BooleanField(default=False)),
                ('question2', models.BooleanField(default=False)),
                ('question3', models.BooleanField(default=False)),
                ('question4', models.BooleanField(default=False)),
                ('question5', models.BooleanField(default=False)),
                ('question6', models.BooleanField(default=False)),
                ('question7', models.BooleanField(default=False)),
                ('question8', models.BooleanField(default=False)),
                ('question9', models.BooleanField(default=False)),
                ('question10', models.BooleanField(default=False)),
                ('question11', models.BooleanField(default=False)),
                ('question12', models.BooleanField(default=False)),
                ('question13', models.BooleanField(default=False)),
                ('question14', models.BooleanField(default=False)),
                ('question15', models.BooleanField(default=False)),
                ('question16', models.BooleanField(default=False)),
                ('question17', models.BooleanField(default=False)),
                ('question18', models.BooleanField(default=False)),
                ('question19', models.BooleanField(default=False)),
                ('question20', models.BooleanField(default=False)),
                ('question21', models.BooleanField(default=False)),
                ('question22', models.BooleanField(default=False)),
                ('question23', models.BooleanField(default=False)),
                ('question24', models.BooleanField(default=False)),
                ('question25', models.BooleanField(default=False)),
            ],
        ),
    ]