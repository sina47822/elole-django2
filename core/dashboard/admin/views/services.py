from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.views.generic import (
    View,
    TemplateView,
    UpdateView,
    ListView,
    DeleteView,
    CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from dashboard.admin.forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from accounts.models import Profile
from django.shortcuts import redirect
from django.contrib import messages
from stylist.models import Services, ServiceCategoryModel, ServiceStatusType
from django.core.exceptions import FieldError


class AdminServiceListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/services/service-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = Services.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(name__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["categories"] = ServiceCategoryModel.objects.all()
        return context


class AdminServiceCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/services/service-create.html"
    queryset = Services.objects.all()
    form_class = ServiceForm
    success_message = "ایجاد خدمت با موفقیت انجام شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:admin:service-edit", kwargs={"pk": form.instance.pk}))

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:service-list")


class AdminServiceEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/services/service-edit.html"
    queryset = Services.objects.all()
    form_class = ServiceForm
    success_message = "ویرایش خدمت با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:service-edit", kwargs={"pk": self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_form"] = ServiceImageForm()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.service_images.prefetch_related()
        return obj


class AdminServiceDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/admin/services/service-delete.html"
    queryset = Services.objects.all()
    success_url = reverse_lazy("dashboard:admin:service-list")
    success_message = "حذف خدمت با موفقیت انجام شد"


class AdminServiceAddImageView(LoginRequiredMixin, HasAdminAccessPermission, CreateView):
    http_method_names = ['post']
    form_class = ServiceImageForm

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:service-edit', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        return ServiceImageForm.objects.filter(service__id=self.kwargs.get('pk'))

    def form_valid(self, form):
        form.instance.service = Services.objects.get(
            pk=self.kwargs.get('pk'))
        # handle successful form submission
        messages.success(
            self.request, 'تصویر مورد نظر با موفقیت ثبت شد')
        return super().form_valid(form)

    def form_invalid(self, form):
        # handle unsuccessful form submission
        messages.error(
            self.request, 'اشکالی در ارسال تصویر رخ داد لطفا مجدد امتحان نمایید')
        return redirect(reverse_lazy('dashboard:admin:service-edit', kwargs={'pk': self.kwargs.get('pk')}))


class AdminServiceRemoveImageView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    http_method_names = ["post"]
    success_message = "تصویر مورد نظر با موفقیت حذف شد"

    def get_queryset(self):
        return ServiceImageModel.objects.filter(service__id=self.kwargs.get('pk'))
    
    def get_object(self, queryset=None):
        return self.get_queryset().get(pk=self.kwargs.get('image_id'))

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:service-edit', kwargs={'pk': self.kwargs.get('pk')})

    def form_invalid(self, form):
        messages.error(
            self.request, 'اشکالی در حذف تصویر رخ داد لطفا مجدد امتحان نمایید')
        return redirect(reverse_lazy('dashboard:admin:service-edit', kwargs={'pk': self.kwargs.get('pk')}))
