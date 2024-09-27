from django import forms
from reserveform.models import ReserveFormModel

class ReservationForm(forms.ModelForm):
    class Meta:
        model = ReserveFormModel
        fields = ['customer','stylist','service','service_category','day','hour']

class ReservationForm2(forms.ModelForm):
    class Meta:
        model = ReserveFormModel
        fields = ['stylist']
class ReservationForm4(forms.ModelForm):
    class Meta:
        model = ReserveFormModel
        fields = [ 'service']
class ReservationForm3(forms.ModelForm):
    class Meta:
        model = ReserveFormModel
        fields = ['service_category']
class ReservationForm5(forms.Form):
    class Meta:
        model = ReserveFormModel
        fields = ['day']
class ReservationForm6(forms.ModelForm):
    class Meta:
        model = ReserveFormModel
        fields = ['hour']