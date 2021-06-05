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


class StaffDB(models.Model):
    no = models.IntegerField(blank=False,null=False)
    fullName = models.CharField(max_length=50,blank=False,null=False)
    kanaName = models.CharField(max_length=50,blank=True,null=True)
    staffDivision1 = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='staffDivision1',blank=False,null=False) 
    staffDivision2 = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='staffDivision2',blank=True,null=True) 
    staffDivision3 = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='staffDivision3',blank=True,null=True) 

    class Meta:
        ordering = ('no',)

    def __str__(self):
        return str(self.no) + self.fullName 
