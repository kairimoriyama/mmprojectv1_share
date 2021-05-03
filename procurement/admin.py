
from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportMixin

from .models import AdminCheck, Category1, Category2, Division, DeliveryAddress, OrderRequest, OrderInfo, Payment, Progress, Supplier, StandardItem
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

class Category1Admin(ImportExportModelAdmin, admin.ModelAdmin):
    class Category1Resource(resources.ModelResource):
        class Meta:
            model = Category1
            fields = ('id','no', 'name')
    resource_class = Category1Resource

class Category2Admin(ImportExportModelAdmin, admin.ModelAdmin):
    class Category2Resource(resources.ModelResource):
        class Meta:
            model = Category2
            fields = ('id','no', 'name', 'category1', )
    resource_class = Category2Resource


class ProgressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ProgressResource(resources.ModelResource):
        class Meta:
            model = Progress
            fields = ('id','no', 'name')
    resource_class = ProgressResource

class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class PaymentResource(resources.ModelResource):
        class Meta:
            model = Payment
            fields = ('id','no', 'name')
    resource_class = PaymentResource



class SupplierAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class SupplierResource(resources.ModelResource):
        class Meta:
            model = Supplier
            fields = ('id','no', 'name', 'tel', 'email', 
            'webpageURL', 'commonId', 'commonPass', 'description')
    resource_class = SupplierResource

class StandardItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class StandardItemResource(resources.ModelResource):
        class Meta:
            model = StandardItem
            fields = ('id','no', 'name', 'category2', 'description',
             'price', 'picture1', 'picture2', 'refURL1', 'refURL2', 'supplier')
    resource_class = StandardItemResource


class OrderRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class OrderRequestResource(resources.ModelResource):
        class Meta:
            model = OrderRequest
            fields = ('id','requestNum', 'submissionDate',
            'requestStaffDivision', 'requestStaff',
            'adminCheck', 'adminStaff',
            'dueDate', 'deliveryAddress', 
            'costCenter1', 'costCenter2', 'costCenter3', 
            'requestDescription', 'itemCategory1', 'itemCategory2', 
            'standardItem', 'quantity', 
            'estimatedAmount', 'refURL1', 'refURL2', 'refURL3',
            'adminDescription',
            'deletedItem'
            )
    resource_class = OrderRequestResource


class OrderInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class OrderInfoResource(resources.ModelResource):
        class Meta:
            model = OrderInfo
            fields = ('id','orderNum', 'orderDate',
            'orderRequest', 'progress', 'orderStaff',
            'orderStaffDivision', 'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totlaAmount', 'payment', 'orderDescription', 
            'acceptanceDate', 'acceptanceStaff', 'acceptanceStaffDivision', 
            'acceptanceMemo','deletedItem'
            )
    resource_class = OrderInfoResource


admin.site.register(Division, DivisionAdmin)
admin.site.register(DeliveryAddress, DeliveryAddressAdmin)

admin.site.register(AdminCheck, AdminCheckAdmin)
admin.site.register(Category1, Category1Admin)
admin.site.register(Category2, Category2Admin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(StandardItem, StandardItemAdmin)

admin.site.register(OrderRequest, OrderRequestAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)



