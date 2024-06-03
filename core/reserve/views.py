from urllib import request
from django.shortcuts import render
from django.views import View
from reserve.forms import ReservationForm
from reserve.models import Reservation

class ReservationCreateView(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, 'reservation-form.html', {'form': form})
    