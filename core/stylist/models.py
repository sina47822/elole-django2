from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator

class ServiceStatusType(models.IntegerChoices):
    publish = 1 ,("نمایش")
    draft = 2 ,("عدم نمایش")


class ServiceCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    image = models.ImageField(upload_to='services/category/', null = True, blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_date"]
        
    def __str__(self):
        return self.title

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
    slug = models.SlugField(allow_unicode=True, null = True, blank = True , unique=True)
    category = models.ManyToManyField(ServiceCategoryModel, related_name=('category'))
    user = models.ForeignKey("accounts.User",on_delete=models.PROTECT)
    description = models.TextField(null = True, blank = True)
    image = models.ImageField(upload_to='services/', null = True, blank = True)
    brief_description = models.TextField(null=True,blank=True)
    duration = models.IntegerField(null=True,blank=True)

    stock = models.PositiveIntegerField(default=0)

    stylist = models.ManyToManyField('Stylist',blank = True,related_name='stylist')
    discount_percent = models.IntegerField(default=0,validators = [MinValueValidator(0),MaxValueValidator(100)])
    status = models.IntegerField(choices=ServiceStatusType.choices,default=ServiceStatusType.draft.value)
    price = models.DecimalField(default=0,max_digits=10,decimal_places=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('stylist:services', kwargs={'slug': self.slug})
    
    class Meta:
        ordering = ["-created_date"]
        
    def __str__(self):
        return self.name
    
    def get_price(self):        
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        discounted_amount = self.price - discount_amount
        return round(discounted_amount)
    
    def is_discounted(self):
        return self.discount_percent != 0
    
    def is_published(self):
        return self.status == ServiceStatusType.publish.value
    

class Stylist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stylist_profile')
    skills = models.ManyToManyField(Skills,blank = True,related_name='skills')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    instagram = models.CharField(max_length=255,blank=True, null=True)
    word_day = models.ManyToManyField('WorkDay',blank=True)
    special_work_times = models.ManyToManyField('SpecificWorkHour',blank=True)

    def __str__(self):
        if self.user.email:
            return self.user.email
        else :
            return self.user.phone_number

class PortfolioImage(models.Model):
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='portfolio_images')
    image = models.ImageField(upload_to='portfolio/')
    title = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

HOUR_OF_DAY_24 = [(i,i) for i in range(1,25)]

WEEKDAYS = [
  (1, _("Saturday")),
  (2, _("Sunday")),
  (3, _("Monday")),
  (4, _("Tuesday")),
  (5, _("Wednesday")),
  (6, _("Thursday")),
  (7, _("Friday")),
]
class SpecificWorkHour(models.Model):
    from_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, null=True, blank=True)
    to_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, null=True, blank=True)
    add_remove = models.BooleanField(default=True)  # True = add, False = subtract
    date = models.DateField()
    hours = models.ManyToManyField('WorkHour',blank=True)

    def __str__(self):
        return f"{self.date} - {self.add_remove} ({'Add' if self.pros_minus else 'Remove'})"

class WorkDay(models.Model):
    day = models.DateField()
    weekday_from = models.PositiveSmallIntegerField(choices=WEEKDAYS,null=True,blank=True)
    weekday_to = models.PositiveSmallIntegerField(choices=WEEKDAYS,null=True,blank=True)
    hours = models.ManyToManyField('WorkHour',blank=True)

    def __str__(self):
        return f'{self.day}'
    
class WorkHour(models.Model):
    from_hour = models.IntegerField(choices=HOUR_OF_DAY_24,null=True,blank=True)
    to_hour = models.IntegerField(choices=HOUR_OF_DAY_24,null=True,blank=True)

    def __str__(self):
        return f'{self.from_hour} - {self.to_hour}'
    # class Meta:
    #     ordering = ('weekday', 'from_hour')
    #     unique_together = ('weekday', 'from_hour', 'to_hour')

    #     def __unicode__(self):
    #         return u'%s: %s - %s' % (self.get_weekday_display(),
    #                                 self.from_hour, self.to_hour)

class ServiceImageModel(models.Model):
    service = models.ForeignKey(Services,on_delete=models.CASCADE,related_name="service_images")
    file = models.ImageField(upload_to="service/extra-img/")
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_date"]
class WishlistServicesModel(models.Model):
    user = models.ForeignKey("accounts.User",on_delete=models.PROTECT)
    service = models.ForeignKey(Services,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.service.title