from django.db import models
from django.utils import timezone
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from django_resized import ResizedImageField
from staffdb.models import StaffDB, Division


class Progress(models.Model):
    no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=50)
    
    class Meta:
        ordering = ('no',)

    def __str__(self):
        return self.name


class Category(models.Model):
    no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('no',)

    def __str__(self):
        return self.name




class ItemManager(models.Manager):


    def all_list(self):
        return super().get_queryset(
        ).filter(deletedItem=False
        )

    def due_list(self):
        return super().get_queryset(
        ).filter(deletedItem=False
        ).filter(ideaNum__gt=0
        ).exclude(dueDate__isnull=True
        ).order_by('dueDate','itemNum')


# 削除されていないデータ 期日のあるデータ システム案件 だけをクエリセットとして選択
class ItemQuerySet(models.QuerySet):

    def item_all(self):
        return self.all()

    def item_alive(self):
        return self.filter(deletedItem=False)

    def item_due(self):
        return self.filter(dueDate__isnull=False)

    def item_system(self):
        return self.filter(system__exact=True)  

class Item(models.Model):
    itemNum =  models.IntegerField(blank=False,null=False, default=0)
    ideaNum = models.IntegerField(blank=True,null=True, default=0)
    actionNum = models.IntegerField(blank=True,null=True, default=0)
    submissionDate = models.DateField(default=timezone.now, blank=True)
    progress = models.ForeignKey(Progress,on_delete=models.PROTECT,
        related_name ='item_progress', blank=False,null=False)
    # 後でblank=False,null=Falseに修正
    division = models.ForeignKey(Division,on_delete=models.PROTECT,
        related_name ='item_dividion', blank=True,null=True)     

    # foreignkey で staff情報を管理 
    staff = models.CharField(max_length=100, blank=True,null=True)
    staffdb =  models.ForeignKey(StaffDB,on_delete=models.PROTECT,
        related_name ='item_staffdb', blank=True,null=True)

    category = models.ForeignKey(Category,on_delete=models.PROTECT,
        related_name ='item_category', blank=False,null=False)
    system = models.BooleanField(default=False)
    purchase = models.BooleanField(default=False)
    title = models.TextField(max_length=2500, blank=False,null=False)
    description = models.TextField(max_length=2500, blank=False,null=False)

    refURL1 = models.URLField(max_length=1800, blank=True,null=True)
    refURL2 = models.URLField(max_length=1800, blank=True,null=True)
    refURL3 = models.URLField(max_length=1800, blank=True,null=True)

    picture1 = ResizedImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)
    picture2 = ResizedImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)
    picture3 = ResizedImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)
    picture4 = ResizedImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)
    picture5 = ResizedImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)
    picture6 = ResizedImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)

    refFile1 = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)
    refFile2 = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)
    refFile3 = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)

    discussionDate = models.DateField(blank=True,null=True)
    discussionNote = models.TextField(max_length=2500, blank=True,null=True)
    report = models.TextField(max_length=2500, blank=True,null=True)
    inchargeDivision = models.CharField(max_length=50, blank=True,null=True)
    inchargeStaff = models.CharField(max_length=50, blank=True,null=True)
    internalDiscussion = models.BooleanField(default=False)
    completionDate = models.DateField(blank=True,null=True)
    dueDate = models.DateField(blank=True,null=True)
    adminMemo = models.CharField(max_length=100, blank=True,null=True)
    deletedItem = models.BooleanField(default=False)
 
    # all_list due_list --> ListViewで抽出
    objects_list = ItemManager()

    # prev next でidea action の移動を区別
    objects = ItemQuerySet.as_manager()

    def __str__(self):
        return self.title  

    def get_absolute_url(self):
        return reverse('goodidea:detail_filter', args=[self.id])

    def get_prev_item_by_itemNum(self):
        """前のitemNumのitemを取得"""
        return type(self).objects.item_alive(
        ).filter(itemNum__gt=self.itemNum
        ).order_by('itemNum').first()

    def get_next_item_by_itemNum(self):
        """次のitemNumのitemを取得"""
        return type(self).objects.item_alive(
        ).filter(itemNum__lt=self.itemNum
        ).order_by('itemNum').last()


    # dueDate DetailView 日付で並び替え

    def get_prev_idea_by_dueDate(self):
        """期日が空欄ではない前のideaを取得"""

        if type(self).objects.item_alive(
            ).item_due(
            ).filter(dueDate__exact=self.dueDate,itemNum__lt=self.itemNum
            ).order_by('itemNum').last():

            return type(self).objects.item_alive(
            ).item_due(
            ).filter(dueDate__exact=self.dueDate,itemNum__lt=self.itemNum
            ).order_by('itemNum').last()

        
        else:

            return type(self).objects.item_alive(
            ).item_due(
            ).filter(dueDate__lt=self.dueDate
            ).order_by('dueDate','itemNum').last()
            

    def get_next_idea_by_dueDate(self):
        """期日が空欄ではない次のideaを取得"""

        if type(self).objects.item_alive(
            ).item_due(
            ).filter(dueDate__exact=self.dueDate, itemNum__gt=self.itemNum
            ).first():

            return type(self).objects.item_alive(
            ).item_due(
            ).filter(dueDate__exact=self.dueDate, itemNum__gt=self.itemNum
            ).first()

        
        else:

            return type(self).objects.item_alive(
            ).item_due(
            ).filter(dueDate__gt=self.dueDate
            ).order_by('dueDate','itemNum').first()
