from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportMixin

from .models import Division, StaffDB
# Register your models here.

class DivisionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class DivisionResource(resources.ModelResource):
        class Meta:
            model = Division
            fields = ('id','no', 'name')
    resource_class = DivisionResource


class StaffDBAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class StaffDBResource(resources.ModelResource):
        class Meta:
            model = StaffDB
            fields = ('id','no', 'fullName', 'kanaName', 'staffDivision1', 'staffDivision2', 'staffDivision3')
    resource_class = StaffDBResource

admin.site.register(Division, DivisionAdmin)
admin.site.register(StaffDB, StaffDBAdmin)
