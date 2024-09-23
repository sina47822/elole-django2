from django.urls import path,re_path
from .views import ReserveFormView,ReservationConfirmView,reservation_form_category,reservation_form_service,reservation_form_stylist,reservation_form_workday,reservation_form_workhour,reservation_form_review
from django.views.generic import TemplateView

app_name = 'reserveform'

urlpatterns = [
    path("",ReserveFormView.as_view(),name="reservation_form"),
    path('confirm/', ReservationConfirmView.as_view(), name='reservation_confirm'),
    path('success/', TemplateView.as_view(template_name="formreserve/reserve-success.html"), name='reservation_success'),
    path('failed/', TemplateView.as_view(template_name="formreserve/reserve-failed.html"), name='reservation_failed'),


    path("category/",reservation_form_category,name="category"),
    path("services/",reservation_form_service,name="services"),
    path("stylist/",reservation_form_stylist,name="stylist"),
    path("workday/",reservation_form_workday,name="workday"),
    path("workhour/",reservation_form_workhour,name="workhour"),
    path("review/",reservation_form_review,name="review"),


]