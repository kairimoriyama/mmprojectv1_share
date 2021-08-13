from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportMixin

from .models import ARCheck, ProjectProgress, ProjectCategory, ClientCategory, Client, Settlement, Project
# Register your models here.



class ARCheckAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ARCheckResource(resources.ModelResource):
        class Meta:
            model = ARCheck
            fields = ('id','no', 'name')
    resource_class = ARCheckResource




class ProjectProgressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ProjectProgressResource(resources.ModelResource):
        class Meta:
            model = ProjectProgress
            fields = ('id','no', 'name')
    resource_class = ProjectProgressResource


class ProjectCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ProjectCategoryResource(resources.ModelResource):
        class Meta:
            model = ProjectCategory
            fields = ('id','no', 'name')
    resource_class = ProjectCategoryResource


class ClientCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ClientCategoryResource(resources.ModelResource):
        class Meta:
            model = ClientCategory
            fields = ('id','no', 'name')
    resource_class = ClientCategoryResource


class ClientAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ClientResource(resources.ModelResource):
        class Meta:
            model = Client
            fields = ('id','no', 'registeredDate',
            'fullName', 'kanaName', 'zipcode', 'address1',
            'address2', 'clientCategory', 'description', 'refURL1', 'refURL2')
    resource_class = ClientResource


class SettlementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class SettlementResource(resources.ModelResource):
        class Meta:
            model = Settlement
            fields = ('id','no', 'statement', 'arCheck',
            'amountOnstatement','transferFee','otherAmount',
            'memo','refFile','deletedItem')
    resource_class = SettlementResource


class ProjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ProjectResource(resources.ModelResource):
        class Meta:
            model = Project
            fields = ('id','projectNum', 'projectProgress', 'createdDate',
            'quotationDate','quotationNum', 'invoiceDate','invoiceNum',
            'client', 'mSatffDivision', 'mSatff', 
            'staff1', 'staff2','staff3','assistant1','assistant2', 'assistant3',
            'salesAmount1', 'salesAmount2', 'salesAmount3', 'salesTotal', 
            'costAmount1', 'costAmount2', 'costAmount3', 'costATotal', 
            'projectcategory', 'projectName', 'description',
            'projectPeriodFrom', 'projectPeriodTo', 'projectPeriodDetail', 'location',
            'picture1', 'picture2', 'picture3', 'picture4', 'picture5', 'picture6',
            'refURL1', 'refURL2', 'refURL3', 'refFile1', 'refFile2', 'refFile3',
            'adminDescription', 'deletedItem',
            )
    resource_class = ProjectResource



admin.site.register(ARCheck, ARCheckAdmin)
admin.site.register(ProjectProgress, ProjectProgressAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(ClientCategory, ClientCategoryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Settlement, SettlementAdmin)
admin.site.register(Project, ProjectAdmin)