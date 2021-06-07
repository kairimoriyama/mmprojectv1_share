from django.db import models
from django.utils import timezone
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class Division(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        ordering = ('no',)

    def __str__(self):
        return self.name


# 削除されていないスタッフ 在職中スタッフ だけを選択
class StaffManager(models.Manager):

    def active_list(self):
        return super().get_queryset(
        ).filter(deletedItem=False).exclude(no__exact=99999999)

# 削除されていないスタッフ 在職中スタッフ だけをクエリセットとして選択
class StaffQuerySet(models.QuerySet):

    def staff_all(self):
        return self.all()

    def staff_active(self):
        return self.filter(deletedItem=False).exclude(no__exact=99999999)

class StaffDB(models.Model):
    no = models.IntegerField(blank=False,null=False)
    fullName = models.CharField(max_length=50,blank=False,null=False)
    kanaName = models.CharField(max_length=50,blank=True,null=True)
    staffDivision1 = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='staffDivision1',blank=True,null=True) 
    staffDivision2 = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='staffDivision2',blank=True,null=True) 
    staffDivision3 = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='staffDivision3',blank=True,null=True) 
    deletedItem = models.BooleanField(default=False)


    objects_list = StaffManager()
    objects = StaffQuerySet.as_manager()

    class Meta:
        ordering = ('kanaName',)

    def __str__(self):
        return self.fullName 
