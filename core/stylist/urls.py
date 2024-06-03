from django.urls import path
from stylist.views import ServicesView, StylistView,ServicesListView,StylistListView
app_name = 'stylist'

urlpatterns = [
    path('services/', ServicesListView , name='services-list'),
    path('services/<slug:slug>', ServicesView , name='services'),
    path('stylist/', StylistListView , name='stylist-list'),
    path('stylist/<int:pk>/', StylistView , name='stylist-account'),


]