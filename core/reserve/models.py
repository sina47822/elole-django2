from django.db import models
from django.urls import reverse
from stylist.models import Services,Stylist,WorkDay,WorkHour
from customer.models import CustomerUser
class Reservation(models.Model):
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='reservations')
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='reservations')
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    status = models.ForeignKey( 'Reservation_status' , on_delete=models.CASCADE , null=True)
    paid = models.ForeignKey( 'Reservation_paid' , on_delete=models.CASCADE , null=True)
    day = models.ForeignKey(WorkDay, on_delete=models.CASCADE)
    hour = models.ForeignKey(WorkHour, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reservation for {self.user.name} with {self.stylist.user.name} on {self.workday.day} at {self.workhour.hour}'

    def get_absolute_url(self):
        return reverse('reservation:detail', kwargs={'pk': self.pk})
class Reservation_status(models.Model):
    status = models.CharField(max_length=100,null=True)

class Reservation_Paid(models.Model):
    paid = models.CharField(max_length=100,null=True)