from django.contrib import admin
from stylist.models import  Address, Services, Skills, WorkDay,WorkHour, PortfolioImage, Stylist,ServiceImageModel,ServiceCategoryModel,WishlistServicesModel

admin.site.register(Address)
admin.site.register(Skills)
admin.site.register(WorkDay)
admin.site.register(WorkHour)

class WorkDayInline(admin.TabularInline):
    model = WorkDay
    extra = 1
    fields = ['day']

class StylistAdmin(admin.ModelAdmin):
    inlines = [WorkDayInline]

admin.site.register(PortfolioImage)
admin.site.register(Stylist, StylistAdmin)

@admin.register(Services)
class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status","stock","price","discount_percent", "created_date")

@admin.register(ServiceCategoryModel)
class ServiceCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id","image", "title", "created_date")

@admin.register(ServiceImageModel)
class ServiceImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_date")

@admin.register(WishlistServicesModel)
class WishlistServiceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "service")

