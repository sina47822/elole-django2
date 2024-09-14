from django.urls import path,re_path
from . import views
from .forms import ReservationForm

app_name = 'reserveform'

urlpatterns = [
    path("",views.ReserveFormView.as_view(),name="form-wizard"),
    # path("reserve/", views.ReserveFormPreview(ReservationForm),name="form-preview"),

]