from django.contrib import admin

# Register your models here.
from .models import ErrorReport

@admin.register(ErrorReport)  # este admin es para el modelo ErrorReport
class ErrorReportAdmin(admin.ModelAdmin):
    # lo que se ve en la lista de errores 
    list_display = ['id', 'code', 'description', 'date']
    # filtros para buscar rapido 
    list_filter = ['code', 'date']
    # busca en descripcion y codigo
    search_fields = ['description', 'code']
    # navegacion por fechas (aparece arriba)
    date_hierarchy = 'date'