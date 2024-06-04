from django.urls import path, include
from .. import views


urlpatterns = [
    path("service/list/",views.AdminServiceListView.as_view(),name="service-list"),
    path("service/create/",views.AdminServiceCreateView.as_view(),name="service-create"),
    path("service/<int:pk>/edit/",views.AdminServiceEditView.as_view(),name="service-edit"),
    path("service/<int:pk>/delete/",views.AdminServiceDeleteView.as_view(),name="service-delete"),
    path("service/<int:pk>/add-image/",views.AdminServiceAddImageView.as_view(),name="service-add-image"),
    path("service/<int:pk>/image/<int:image_id>/remove/",views.AdminServiceRemoveImageView.as_view(),name="service-remove-image"),
]
