from django.db import models
from stylist.models import Services,Stylist,WorkDay,WorkHour,ServiceCategoryModel
from accounts.models import User


class ReserveFormModel(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserveform', blank=True, null=True)
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='reserveform', blank=True, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, blank=True, null=True)
    service_category = models.ForeignKey(ServiceCategoryModel,on_delete=models.CASCADE, blank=True, null=True )
    status = models.ForeignKey( 'ReserveForm_status' , on_delete=models.CASCADE , null=True, blank=True)
    paid = models.ForeignKey( 'ReserveForm_paid' , on_delete=models.CASCADE , null=True, blank=True)
    day = models.CharField(max_length=30,null=True, blank=True)
    hour = models.CharField(max_length=30,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'reserveform for {self.stylist.user.first_name} with {self.stylist.user.last_name}'

class ReserveForm_status(models.Model):
    status = models.CharField(max_length=100,null=True)

class ReserveForm_Paid(models.Model):
    paid = models.CharField(max_length=100,null=True)
# Create your models here.
