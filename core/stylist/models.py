from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from accounts.models import User

class Address(models.Model):
    city = models.CharField(max_length=100)
    address_title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.city}, {self.address_title}, {self.address}'

class Skills (models.Model):
    title = models.CharField( max_length=250)
    image = models.ImageField(upload_to='skills/', null = True, blank = True)

    def __str__(self):
        return self.title
    
class Services(models.Model):
    name= models.CharField(max_length=200)
    slug = models.SlugField(max_length = 250, null = True, blank = True , unique=True)
    cost = models.IntegerField(null=True , blank=True)
    description = models.TextField(null = True, blank = True)
    image = models.ImageField(upload_to='services/', null = True, blank = True)
    stylist = models.ManyToManyField('Stylist',blank = True,related_name='stylist')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stylist:services', kwargs={'slug': self.slug})


class Stylist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stylist_profile')
    services = models.ManyToManyField(Services,blank = True,related_name='services')
    skills = models.ManyToManyField(Skills,blank = True,related_name='skills')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    instagram = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        if self.user.name:
            return self.user.name
        else :
            return self.user.username

class PortfolioImage(models.Model):
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='portfolio_images')
    image = models.ImageField(upload_to='portfolio/')
    title = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class WorkDay(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    stylist = models.ForeignKey(Stylist, on_delete=models.SET_NULL, related_name='work_time',null=True,blank=True)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    hour = models.ManyToManyField('WorkHour', related_name='work_hours')

    def __str__(self):
        return self.day

class WorkHour(models.Model):
    DAY_CHOICES = [
        ('9:30 to 10:30', '9:30 to 10:30'),
        ('10:30 to 11:30', '10:30 to 11:30'),
        ('11:30 to 12:30', '11:30 to 12:30'),
        ('12:30 to 13:30', '12:30 to 13:30'),
        ('13:30 to 14:30', '13:30 to 14:30'),
        ('14:30 to 15:30', '14:30 to 15:30'),
        ('15:30 to 16:30', '15:30 to 16:30'),
    ]
    hour = models.CharField(max_length=150,choices=DAY_CHOICES, null=True , blank=True)

    def __str__(self):
        return self.hour
