from django import forms
from stylist.models import CustomerUser


class CustomerUserAdmin(forms.Form):
    name= forms.CharField(max_length=200 )
    lastname= forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    email = forms.SlugField(max_length = 250, unique=True)
    phone = forms.CharField(max_length=15)
    image = forms.ImageField(upload_to='customer_profile/', height_field='100px', width_field='100px')
