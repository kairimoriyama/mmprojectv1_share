
from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportMixin

from .models import Category, Progress, Item
# Register your models here.



class ItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ItemResource(resources.ModelResource):
        class Meta:
            model = Item
            fields = ('id','itemNum','ideaNum','actionNum','submissionDate','progress',
            'division','staff','staffdb','category','system','purchase','title','description',
            'refURL1','refURL2','refURL3',
            'picture1','picture2','picture3','picture4','picture5','picture6',
            'refFile1','refFile2','refFile3',
            'discussionDate','discussionNote','report',
            'inchargeDivision','inchargeStaff','internalDiscussion','completionDate','dueDate','adminMemo','deletedItem')
    resource_class = ItemResource



class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class CategoryResource(resources.ModelResource):
        class Meta:
            model = Category
            fields = ('id','no', 'name')
    resource_class = CategoryResource

class ProgressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class ProgressResource(resources.ModelResource):
        class Meta:
            model = Progress
            fields = ('id','no', 'name')
    resource_class = ProgressResource





admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Progress, ProgressAdmin)

