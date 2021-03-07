from django.db import models
from django.utils import timezone
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class Progress(models.Model):
    no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Division(models.Model):
    no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name




class ItemManager(models.Manager):

    def idea_list(self):
        return super().get_queryset(
        ).filter(deletedItem=False
        ).filter(ideaNum__gt=0)
        
    def action_list(self):
        return super().get_queryset(
        ).filter(deletedItem=False
        ).filter(actionNum__gt=0)


class ItemQuerySet(models.QuerySet):

    def item_all(self):
        return self.all()

    def item_alive(self):
        return self.filter(deletedItem=False)

    def item_idea(self):
        return self.filter(ideaNum__gt=0)

    def item_action(self):
        return self.filter(actionNum__gt=0)
        

class Item(models.Model):
    itemNum =  models.IntegerField(blank=True,null=True)
    ideaNum = models.IntegerField(blank=True,null=True, default=0)
    actionNum = models.IntegerField(blank=True,null=True, default=0)
    submissionDate = models.DateField(default=timezone.now, blank=True)
    progress = models.ForeignKey(Progress,on_delete=models.PROTECT, related_name ='item_progress')
    division = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='item_dividion')     
    staff = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.PROTECT, related_name ='item_category')
    title = models.TextField(max_length=2500)
    description = models.TextField(max_length=2500)

    refURL1 = models.URLField(blank=True,max_length=300)
    refURL2 = models.URLField(blank=True,max_length=300)
    refURL3 = models.URLField(blank=True,max_length=300)

    picture1 = models.ImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)
    picture2 = models.ImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)
    picture3 = models.ImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)

    refFile1 = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)
    refFile2 = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)
    refFile3 = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)

    discussionDate = models.DateField(blank=True,null=True)
    discussionNote = models.TextField(max_length=2500, blank=True)
    report = models.TextField(max_length=2500, blank=True)
    inchargeDivision = models.CharField(max_length=50,blank=True)
    inchargeStaff = models.CharField(max_length=50,blank=True)
    completionDate = models.DateField(blank=True,null=True)
    adminMemo = models.CharField(max_length=100,blank=True)
    deletedItem = models.BooleanField(default=False)
 
    # idea_list action_list --> ListView
    objects_list = ItemManager()

    # prev next でidea action の移動を区別
    objects = ItemQuerySet.as_manager()

    def __str__(self):
        return self.title  

    def get_absolute_url(self):
        return reverse('goodidea:detail_item', args=[self.id])



    def get_prev_item_by_itemNum(self):
        """前のitemNumのitemを取得"""
        return type(self).objects.item_alive().filter(itemNum__lt=self.itemNum).order_by('itemNum').last()

    def get_next_item_by_itemNum(self):
        """次のitemNumのitemを取得"""
        return type(self).objects.item_alive().filter(itemNum__gt=self.itemNum).order_by('itemNum').first()



    def get_prev_idea_by_itemNum(self):
        """前のideaを取得"""
        return type(self).objects.item_alive().item_idea().filter(ideaNum__lt=self.ideaNum).order_by('itemNum').last()

    def get_next_idea_by_itemNum(self):
        """次のideaを取得"""
        return type(self).objects.item_alive().item_idea().filter(ideaNum__gt=self.ideaNum).order_by('itemNum').first()


    def get_prev_action_by_itemNum(self):
        """前のactionを取得"""
        return type(self).objects.item_alive().item_action().filter(actionNum__lt=self.actionNum).order_by('itemNum').last()

    def get_next_action_by_itemNum(self):
        """次のactoinを取得"""
        return type(self).objects.item_alive().item_action().filter(actionNum__gt=self.actionNum).order_by('itemNum').first()