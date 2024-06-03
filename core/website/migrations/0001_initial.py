# Generated by Django 4.2 on 2024-06-03 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='website.category')),
            ],
            options={
                'unique_together': {('slug', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('desc_1', tinymce.models.HTMLField(blank=True, null=True)),
                ('desc_2', tinymce.models.HTMLField(blank=True, null=True)),
                ('post_summery', tinymce.models.HTMLField(blank=True, null=True)),
                ('image', models.ImageField(default='posts/thumbnails/squre_images/1.jpg', upload_to='posts/thumbnails/%Y/%m')),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('publish_date', models.DateTimeField(null=True)),
                ('total_views', models.IntegerField(default=0)),
                ('blog_status', models.CharField(blank=True, choices=[('draft', 'Draft'), ('published', 'Published')], default='Draft', max_length=100, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('categories', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='website.category')),
            ],
            options={
                'ordering': ('-publish_date',),
            },
        ),
        migrations.CreateModel(
            name='SliderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('alt', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='slider/')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TagsSEO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='seo_images/')),
                ('tags_seo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posttags', to='website.tags')),
            ],
        ),
        migrations.CreateModel(
            name='PostSEO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='seo_images/')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='website.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='website.tags'),
        ),
        migrations.CreateModel(
            name='CategorySEO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='seo_images/')),
                ('Category_seo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='postcategory', to='website.category')),
            ],
        ),
    ]
