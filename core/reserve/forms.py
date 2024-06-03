from django import forms
from reserve.models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['stylist', 'service', 'day', 'hour']
