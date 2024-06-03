from django.contrib import admin
from stylist.models import CustomUser, Address, Services, Skills, WorkDay,WorkHour, PortfolioImage, Stylist

admin.site.register(CustomUser)
admin.site.register(Address)
admin.site.register(Services)
admin.site.register(Skills)

class WorkDayTimeInline(admin.TabularInline):
    model = WorkDay
    extra = 1
class WorkHourTimeInline(admin.TabularInline):
    model = WorkHour
    extra = 1

class StylistAdmin(admin.ModelAdmin):
    inlines = [WorkHourTimeInline,WorkDayTimeInline]
    
admin.site.register(PortfolioImage)
admin.site.register(Stylist, StylistAdmin)