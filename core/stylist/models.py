from django.db import models
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager , AbstracBasetUser, PermissionsMixin
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

class StylistUserMAnager(BaseUserManager):
    def createstylist(self,phone,password, **extra_field):
        if not phone :
            raise ValueError(_("phone must be set"))
        pass
    def createsuperstylis(self,phone,password):
        pass
        

class CustomUser(AbstracBasetUser,PermissionsMixin):
    # name= models.CharField(max_length=200 , null = True, blank = True )
    # lastname= models.CharField(max_length=200,null = True, blank = True )
    username = models.CharField(max_length=200 , null=True , unique=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null = True, blank = True )
    email = models.SlugField(max_length = 250, null = True, blank = True , unique=True)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='stylist_profile/', height_field='100px', width_field='100px')
    social_networks = models.JSONField(blank=True, null=True)  # Assuming social networks are stored as JSON
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StylistUserMAnager()

    REQUIRED_FIELD =[]
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stylist:stylist-account', kwargs={'slug': slugify(self.username)})

class Address(models.Model):
    city = models.CharField(max_length=100)
    address_title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.city}, {self.address_title}, {self.address}'

class Skills (models.Model):
    title = models.CharField( max_length=250)
    image = models.ImageField(upload_to='skills/', height_field=None, width_field=None)

    def __str__(self):
        return self.title
    
class Services(models.Model):
    name= models.CharField(max_length=200)
    slug = models.SlugField(max_length = 250, null = True, blank = True , unique=True)
    cost = models.IntegerField(max_length=15 , null=True , blank=True)
    description = models.TextField(null = True, blank = True)
    image = models.ImageField(upload_to='services/', height_field='100px', width_field='100px')
    parent = models.ForeignKey('self' , on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)  # ensures unique slugs in the same parent category

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stylist:services', kwargs={'slug': self.slug})


class Stylist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='stylist_profile')
    services = models.ForeignKey(Services,on_delete=models.DO_NOTHING,blank = True, null = True)
    skills = models.ManyToManyField(Skills,blank = True, null = True)
    is_active = models.BooleanField(default=True)

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
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='work_time')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)

    def __str__(self):
        return f'{self.stylist.user.name} - {self.day}: {self.start_time} - {self.end_time}'

class WorkHour(models.Model):
    DAY_CHOICES = [
        ('9:30 to 10:30', '1'),
        ('10:30 to 11:30', '2'),
        ('11:30 to 12:30', '3'),
        ('12:30 to 13:30', '4'),
        ('13:30 to 14:30', '5'),
        ('14:30 to 15:30', '6'),
        ('15:30 to 16:30', '7'),
    ]
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='work_hour')
    day = models.ForeignKey(WorkDay, on_delete=models.CASCADE, related_name='work_hours', null=True , blank=True)
    hour = models.CharField(choices=DAY_CHOICES, null=True , blank=True)

    def __str__(self):
        return f'{self.stylist.user.name} - {self.day}: {self.start_time} - {self.end_time}'
