# Generated by Django 4.2 on 2024-09-08 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(help_text='لطفا ایمیل خود را اینجا وارد کنید', max_length=254),
        ),
    ]
