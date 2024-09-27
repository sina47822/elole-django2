from django.contrib import admin
from stylist.models import  SpecificWorkHour,Address, Services, Skills, WorkDay,WorkHour, PortfolioImage, Stylist,ServiceImageModel,ServiceCategoryModel,WishlistServicesModel
from import_export.admin import ImportExportModelAdmin

admin.site.register(Address)
admin.site.register(Skills)
admin.site.register(WorkDay)
admin.site.register(WorkHour)
admin.site.register(SpecificWorkHour)


class StylistAdmin(admin.ModelAdmin):
    list_display = ["id", "user","user","is_active","is_staff"]

admin.site.register(PortfolioImage)
admin.site.register(Stylist, StylistAdmin)

@admin.register(Services)
class ServiceModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "status","stock","price","discount_percent", "created_date")

class ServiceCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id","image", "title", "created_date")
admin.site.register(ServiceCategoryModel, ServiceCategoryModelAdmin)

@admin.register(ServiceImageModel)
class ServiceImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_date")

@admin.register(WishlistServicesModel)
class WishlistServiceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "service")

