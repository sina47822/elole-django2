from typing import Any
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from stylist.models import Services, ServiceStatusType
from .cart import CartSession


class SessionAddServiceView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        service_id = request.POST.get("service_id")
        if service_id and Services.objects.filter(id=service_id, status=ServiceStatusType.publish.value).exists():

            cart.add_service(service_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class SessionRemoveServiceView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        service_id = request.POST.get("service_id")
        if service_id:
            cart.remove_service(service_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class SessionUpdateServiceQuantityView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        service_id = request.POST.get("service_id")
        quantity = request.POST.get("quantity")
        if service_id and quantity:
            cart.update_service_quantity(service_id, quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class CartSummaryView(TemplateView):
    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        cart_items = cart.get_cart_items()
        context["cart_items"] = cart_items
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_amount()
        return context