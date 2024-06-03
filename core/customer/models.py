from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from shortuuidfield import ShortUUIDField

from django.db.models.signals import post_save

def user_directory_path(instance,filename):
    ext = filename.splite(".")[-1]
    filename = "%s.%s" % (instance.user.ir, filename)
    return "user_{0}/{1}".format(instance.user.id, filename) 
 
class CustomerUser(AbstractUser):
    name= models.CharField(max_length=200 , null = True, blank = True )
    lastname= models.CharField(max_length=200,null = True, blank = True )
    username = models.CharField(max_length=200 , null = True, blank = True , unique=True)
    email = models.EmailField(max_length = 250, null = True, blank = True , unique=True)
    phone = models.CharField(max_length=13, null = True, blank = True , unique=True)
    image = models.ImageField(upload_to='customer_profile/', height_field='100px', width_field='100px', null = True, blank = True)
    is_stylist = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    otp = models.CharField(max_length=100 , null=True , blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['phone','username','email']
    def __str__(self):
        if self.name :
            return self.name +" "+ self.lastname
        else :
            return self.username
        

    def get_absolute_url(self):
        return reverse('customer:customer-dashboard', kwargs={'slug': slugify(self.email)})

class Profile(models.Model):
    pid = ShortUUIDField(max_length=25,blank=True, editable=False)
    image = models.FileField(upload_to="customer_profile/user_directory_path", default='default.jpg',null=True , blank=True)
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)
    name= models.CharField(max_length=200 , null = True, blank = True )
    lastname= models.CharField(max_length=200,null = True, blank = True )
    phone = models.CharField(max_length=13, null = True, blank = True , unique=True)
    country= models.CharField(max_length=200,null = True, blank = True )
    city= models.CharField(max_length=200,null = True, blank = True )
    address= models.CharField(max_length=200,null = True, blank = True )
    pelak= models.CharField(max_length=200,null = True, blank = True )

    # model_mo=models.CharField(max_length=20,choices=modelmoo)
    wallet = models.DecimalField(max_digits=12,decimal_places=0,default=0)
    verified = models.BooleanField(default=False)
    created_date =models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
    def __str__ (self):
        if self.name:
            return f"(self.name)"
        else:
            return f"(self.user.email)"
def create_user_profile(sender, instance, created, **kewargs):
    if created :
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kewargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=CustomerUser)
post_save.connect(save_user_profile, sender=CustomerUser)

