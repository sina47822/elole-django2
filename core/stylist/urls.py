from django.urls import path, re_path
from . import views

app_name = 'stylist'

urlpatterns = [
    # path('services/', ServicesListView , name='services-list'),
    # path('services/<slug:slug>', ServicesView , name='services'),
    # path('', StylistListView , name='stylist-list'),
    # path('<int:pk>', StylistView , name='stylist-account'),

    path("service/grid/",views.ShopServiceGridView.as_view(),name="service-grid"),
    re_path(r"service/(?P<slug>[-\w]+)/detail/",views.ShopServiceDetailView.as_view(),name="service-detail"),
    path("add-or-remove-wishlist/",views.AddOrRemoveWishlistView.as_view(),name="add-or-remove-wishlist")

]