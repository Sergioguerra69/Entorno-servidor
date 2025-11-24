from django.contrib import admin

# Register your models here.
from .models import ErrorReport

@admin.register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'description', 'date']
    list_filter = ['code', 'date']
    search_fields = ['description', 'code']
    date_hierarchy = 'date'