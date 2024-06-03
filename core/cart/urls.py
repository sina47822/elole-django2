from django.urls import path,re_path
from . import views

app_name = "cart"

urlpatterns = [
    path("session/add-service/",views.SessionAddServiceView.as_view(),name="session-add-service"),
    path("session/remove-service/",views.SessionRemoveServiceView.as_view(),name="session-remove-service"),
    path("session/update-service-quantity/",views.SessionUpdateServiceQuantityView.as_view(),name="session-update-service-quantity"),
    path("summary/",views.CartSummaryView.as_view(),name="cart-summary")
]