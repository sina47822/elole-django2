from django.contrib import admin
from stylist.models import  Address, Services, Skills, WorkDay,WorkHour, PortfolioImage, Stylist

admin.site.register(Address)
admin.site.register(Services)
admin.site.register(Skills)
admin.site.register(WorkDay)
admin.site.register(WorkHour)


class WorkDayTimeInline(admin.TabularInline):
    model = WorkDay
    extra = 1

class StylistAdmin(admin.ModelAdmin):
    inlines = [WorkDayTimeInline]
    
admin.site.register(PortfolioImage)
admin.site.register(Stylist, StylistAdmin)