from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportMixin

from .models import Progress, JournalCategory, AccountType, BankAccount, Statement
# Register your models here.



class ProgressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ProgressResource(resources.ModelResource):
        class Meta:
            model = Progress
            fields = ('id','no', 'name')
    resource_class = ProgressResource


class JournalCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class JournalCategoryResource(resources.ModelResource):
        class Meta:
            model = JournalCategory
            fields = ('id','no', 'name')
    resource_class = JournalCategoryResource

    
class AccountTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class AccountTypeResource(resources.ModelResource):
        class Meta:
            model = AccountType
            fields = ('id','no', 'name')
    resource_class = AccountTypeResource

    
class BankAccountAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class BankAccountResource(resources.ModelResource):
        class Meta:
            model = BankAccount
            fields = ('id','no', 'branchName','accountNumber', 
            'accountType','accountMemo')
    resource_class = BankAccountResource


class StatementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class StatementResource(resources.ModelResource):
        class Meta:
            model = Statement
            fields = ('id','no', 'recordDate',
             'description1', 'description2',
             'paymentAmount', 'deopsitAmount','accountBalance',
             'bankAccount','journalCategory',
             'bankAccount','progress','consistencyCheck',
             )
    resource_class = StatementResource



admin.site.register(Progress, ProgressAdmin)
admin.site.register(JournalCategory, JournalCategoryAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Statement, StatementAdmin)