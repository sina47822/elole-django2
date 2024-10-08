"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from website.sitemaps import StaticViewSitemap,BlogSitemap,BlogTagSitemap,BlogCategorySitemap

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'blogcategory': BlogCategorySitemap,
    'blogtags': BlogTagSitemap,

}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('reserve/', include('reserve.urls')),
    path('stylist/', include('stylist.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls')),
    path('review/', include('review.urls')),
    path('reserveform/', include('reserveform.urls')),


    path('', include('website.urls')),

    path('tinymce/', include('tinymce.urls')),

    path('sitemap.xml', sitemap, {'sitemaps':sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('api/users/', include('kavenegarapp.urls')),
] 

# serving static and media for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



