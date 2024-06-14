from django.shortcuts import get_object_or_404, render
from stylist.models import Stylist,Services,WorkHour,WorkDay,Skills
from django.core.paginator import Paginator

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    View
)
from .models import Services, ServiceStatusType, ServiceCategoryModel, WishlistServicesModel
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from review.models import ReviewModel,ReviewStatusType

def StylistListView(request):
    stylists = Stylist.objects.all().order_by('-id')
    services = Services.objects.all().order_by('-id')[:5]

    paginator = Paginator(stylists, 8)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'stylists': stylists,
                'services':services
               }
    return render(request, 'stylist/stylist-list.html', context)

def StylistView(request, slug): 
    stylist = get_object_or_404(Stylist, slug =slug )
    # seo = StylistSEO.objects.filter(post=post).first()  # Retrieve the first PostSEO object associated with the post
    stylists = Stylist.objects.all().order_by('-id')[:4]
    services = Services.objects.all()
    skills = Skills.objects.all()
    workday = WorkDay.objects.all()
    workhour = WorkHour.objects.all()

    context = {'slug': slug,
               'stylist' : stylist,
               'stylists': stylists,
               'services':services,
               'skills':skills,
               'workday':workday,
               'workhour':workhour,

               }

    return render(request, 'stylist/stylist-detail.html', context) 

# def ServicesListView(request):
#     stylists = Stylist.objects.all()[:5]
#     services = Services.objects.all()

#     paginator = Paginator(services, 4)  # Show 10 posts per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {'stylists': stylists,
#                 'services':services
#                }
#     return render(request, 'stylist/services-list.html', context)

# def ServicesView(request, slug): 
#     service = get_object_or_404(Services, slug =slug )
#     # seo = StylistSEO.objects.filter(post=post).first()  # Retrieve the first PostSEO object associated with the post
#     stylists = Stylist.objects.all().order_by('-id')[:4]
#     services = Services.objects.all()

#     context = {'slug': slug,
#                'service' : service,
#                'stylists': stylists,
#                'services':services,
#                }

#     return render(request, 'stylist/service-detail.html', context) 



# Create your views here.


class ShopServiceGridView(ListView):
    template_name = "stylist/services-list.html"
    paginate_by = 9

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = Services.objects.filter(
            status=ServiceStatusType.publish.value)
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
        context["wishlist_items"] = WishlistServicesModel.objects.filter(user=self.request.user).values_list(
            "service__id", flat=True) if self.request.user.is_authenticated else []
        context["categories"] = ServiceCategoryModel.objects.all()
        return context


class ShopServiceDetailView(DetailView):
    template_name = "stylist/service-detail.html"
    queryset = Services.objects.filter(
        status=ServiceStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        context["is_wished"] = WishlistServicesModel.objects.filter(
            user=self.request.user, service__id=service.id).exists() if self.request.user.is_authenticated else False
        reviews = ReviewModel.objects.filter(service=service,status=ReviewStatusType.accepted.value)
        context["reviews"] = reviews
        total_reviews_count =reviews.count()
        context["reviews_count"] = {
            f"rate_{rate}": reviews.filter(rate=rate).count() for rate in range(1, 6)
        }
        if total_reviews_count != 0:
            context["reviews_avg"] = {
                f"rate_{rate}": round((reviews.filter(rate=rate).count()/total_reviews_count)*100,2) for rate in range(1, 6)
            }
        else:
            context["reviews_avg"] = {f"rate_{rate}": 0 for rate in range(1, 6)}
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.service_images.prefetch_related()
        return obj

class AddOrRemoveWishlistView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        service_id = request.POST.get("service_id")
        message = ""
        if service_id:
            try:
                wishlist_item = WishlistServicesModel.objects.get(
                    user=request.user, service__id=service_id)
                wishlist_item.delete()
                message = "خدمت از لیست علایق حذف شد"
            except WishlistServicesModel.DoesNotExist:
                WishlistServicesModel.objects.create(
                    user=request.user, service_id=service_id)
                message = "خدمت به لیست علایق اضافه شد"

        return JsonResponse({"message": message})
