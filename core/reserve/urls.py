from django.urls import path
from reserve.views import ReservationCreateView


app_name = 'reserve'

urlpatterns = [
    path('', ReservationCreateView.as_view() , name='reservation-form'),
]