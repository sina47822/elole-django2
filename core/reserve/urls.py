from django.urls import path
from reserve.views import ReservationCreateView


app_name = 'reserve'

urlpatterns = [
    path('', ReservationCreateView , name='reservation-form'),
]