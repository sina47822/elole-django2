from django.contrib import admin
from .models import ReviewModel

# Register your models here.

@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "service", "rate","status", "created_date")