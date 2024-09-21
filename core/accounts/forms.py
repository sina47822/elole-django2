from django.contrib.auth import forms as auth_forms
from django import forms

from django.core.exceptions import ValidationError
from accounts.models import User

from kavenegarapp.models import OTPRequest
from kavenegarapp.sender import send_otp  # Assuming you have a module to send OTP

class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)
        
        # if not user.is_verified:
        #     raise ValidationError("user is not verified")

class UserCreationForm_Phone(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number")
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise ValidationError("Passwords do not match.")
        
        # Trigger OTP sending after form validation
        phone_number = cleaned_data.get("phone_number")
        if phone_number:
            otp = OTPRequest.objects.generate({'receiver': phone_number, 'channel': 'phone'})  # This triggers OTP generation
            send_otp(otp)  # Send OTP to the provided phone number

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user