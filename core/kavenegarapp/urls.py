from django.urls import path
from .views import send_otp, verify_otp, OTPView


urlpatterns = [
    path('otp/', OTPView.as_view(), name='otp_view'),

    path('send-otp', send_otp, name='send_otp'),
    path('verify-otp', verify_otp, name='verify_otp'),
]