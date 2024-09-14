from django.contrib import admin
from reserveform.models import ReserveFormModel
# Register your models here.
@admin.register(ReserveFormModel)
class ReserveFormModelAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "stylist", "service","service_category","id", "status", "paid", "day","hour")
