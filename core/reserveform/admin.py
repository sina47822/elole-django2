from django.contrib import admin
from reserveform.models import ReserveFormModel
from reserveform.forms import ReservationForm

# Unregister the model if it's already registered
# admin.site.unregister(ReserveFormModel)

class ReserveFormModelAdmin(admin.ModelAdmin):
    list_display = ("customer", "stylist", "service", "service_category", "status", "paid", "day", "hour")

    def get_form(self, request, obj=None, **kwargs):
        # Use the custom ReservationForm for the admin
        kwargs['form'] = ReservationForm
        return super().get_form(request, obj, **kwargs)

# Register the model again with the custom admin
admin.site.register(ReserveFormModel, ReserveFormModelAdmin)