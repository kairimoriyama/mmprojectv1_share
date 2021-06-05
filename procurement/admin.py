
from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportMixin

from .models import AdminCheck, Division, DeliveryAddress, ItemCategory, OrderRequest, OrderInfo, Purpose, PaymentMethod, Progress, Supplier, StandardItem
# Register your models here.



class DivisionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class DivisionResource(resources.ModelResource):
        class Meta:
            model = Division
            fields = ('id','no', 'name')
    resource_class = DivisionResource


class DeliveryAddressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class DeliveryAddressResource(resources.ModelResource):
        class Meta:
            model = DeliveryAddress
            fields = ('id','no', 'name')
    resource_class = DeliveryAddressResource

class AdminCheckAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class AdminCheckResource(resources.ModelResource):
        class Meta:
            model = AdminCheck
            fields = ('id','no', 'name')
    resource_class = AdminCheckResource

class PurposeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class PurposeResource(resources.ModelResource):
        class Meta:
            model = Purpose
            fields = ('id','no', 'name')
    resource_class = PurposeResource


class ProgressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ProgressResource(resources.ModelResource):
        class Meta:
            model = Progress
            fields = ('id','no', 'name')
    resource_class = ProgressResource

class PaymentMethodAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class PaymentMethodResource(resources.ModelResource):
        class Meta:
            model = PaymentMethod
            fields = ('id','no', 'name')
    resource_class = PaymentMethodResource



class SupplierAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class SupplierResource(resources.ModelResource):
        class Meta:
            model = Supplier
            fields = ('id','no', 'name', 'tel', 'email', 
            'webpageURL', 'commonId', 'commonPass', 'description')
    resource_class = SupplierResource



class ItemCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ItemCategoryResource(resources.ModelResource):
        class Meta:
            model = ItemCategory
            fields = ('id','no', 'name')
    resource_class = ItemCategoryResource

class StandardItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class StandardItemResource(resources.ModelResource):
        class Meta:
            model = StandardItem
            fields = ('id','no', 'name', 'itemCategory', 'description',
             'price', 'picture1', 'picture2', 'refURL1', 'refURL2', 'supplier')
    resource_class = StandardItemResource


class OrderRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class OrderRequestResource(resources.ModelResource):
        class Meta:
            model = OrderRequest
            fields = ('id','requestNum', 'submissionDate',
            'orderInfo',
            'requestStaffDivision', 'requestStaff',
            'adminCheck', 'adminStaff', 
            'dueDate', 'deliveryAddress', 
            'costCenter1', 'costCenter2', 'costCenter3', 
            'purpose', 'standardItem',
            'requestDetail', 'requestMemo', 
            'project', 'approval', 
            'quantity', 'estimatedAmount',
            'refURL1', 'refURL2', 'refURL3',
            'refFile1','refFile2','refFile3',
            'adminDescription', 'deletedItem'
            )
    resource_class = OrderRequestResource


class OrderInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class OrderInfoResource(resources.ModelResource):
        class Meta:
            model = OrderInfo
            fields = ('id','orderNum', 'orderDate',
            'progress', 'orderStaff',
            'orderStaffDivision', 'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totalAmount', 'paymentMethod', 'orderDescription', 
            'acceptanceDate', 'acceptanceStaff', 'acceptanceStaffDivision', 
            'acceptanceMemo',
            'settlementDate','settlement', 'refFile',
            'deletedItem'
            )
    resource_class = OrderInfoResource


admin.site.register(Division, DivisionAdmin)
admin.site.register(DeliveryAddress, DeliveryAddressAdmin)

admin.site.register(AdminCheck, AdminCheckAdmin)
admin.site.register(Purpose, PurposeAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Supplier, SupplierAdmin)

admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(StandardItem, StandardItemAdmin)

admin.site.register(OrderRequest, OrderRequestAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)



