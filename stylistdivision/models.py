from django.db import models
from django.utils import timezone
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from staffdb.models import StaffDB, Division
from bankaccount.models import Statement



class ARCheck(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="ARCheck"
        ordering = ('no',)

    def __str__(self):
        return self.name


class ProjectProgress(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="ProjectProgress"
        ordering = ('no',)

    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="ProjectCategory"
        ordering = ('no',)

    def __str__(self):
        return self.name



class ClientCategory(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="ClientCategory"
        ordering = ('no',)

    def __str__(self):
        return self.name


class Client(models.Model):
    no = models.IntegerField(blank=False,null=False)
    registeredDate = models.DateField(default=timezone.now, blank=True,null=True)
    fullName = models.CharField(max_length=50,blank=False,null=False)
    kanaName = models.CharField(max_length=50,blank=False,null=False)
    zipcode = models.CharField(max_length=10,blank=False,null=False)
    address1 = models.CharField(max_length=50,blank=False,null=False)
    address2 = models.CharField(max_length=50,blank=False,null=False)
    clientCategory = models.ForeignKey(ClientCategory,on_delete=models.PROTECT, related_name ='clientCategory',blank=True,null=True)
    description = models.TextField(max_length=1000, blank=True,null=True)
    refURL1 = models.URLField(max_length=300, blank=True,null=True)
    refURL2 = models.URLField(max_length=300, blank=True,null=True)

    class Meta:
        verbose_name_plural="Client"
        ordering = ('kanaName',)

    def __str__(self):
        return self.fullName


class Settlement(models.Model):
    no =  models.IntegerField(blank=False,null=False)
    statement =  models.ForeignKey(Statement,on_delete=models.PROTECT,
        related_name ='statement',blank=True,null=True)
    arCheck = models.ForeignKey(ARCheck,on_delete=models.PROTECT, related_name ='arCheck',default=1)    

    amountOnstatement = models.IntegerField(blank=True,null=True)
    transferFee = models.IntegerField(blank=True,null=True)
    otherAmount = models.IntegerField(blank=True,null=True)
    totalAmount = models.IntegerField(blank=True,null=True)
    memo = models.TextField(max_length=250,blank=True,null=True)

    refFile = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)
    deletedItem = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="Settlement"

    def __str__(self):
        return str(self.no) + ' ' + str(self.statement.deopsitAmount)+ str(self.statement.description2)



class Project(models.Model):
    projectNum =  models.IntegerField(blank=False,null=False)
    projectProgress = models.ForeignKey(ProjectProgress,on_delete=models.PROTECT, related_name ='project_projectProgress',default=1)    
    createdDate = models.DateField(default=timezone.now, blank=True,null=True)
    quotationDate = models.DateField(default=timezone.now, blank=True,null=True)
    InvoiceDate = models.DateField(default=timezone.now, blank=True,null=True)
    client = models.ForeignKey(Client,on_delete=models.PROTECT, related_name ='project_client',blank=True,null=True) 

    mSatffDivision = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='project_mStaffDivision') 
    mSatff =  models.ForeignKey(StaffDB,on_delete=models.PROTECT,
        related_name ='project_mSatff',blank=True,null=True)

    staff =  models.ManyToManyField(StaffDB, related_name='project_staff',blank=True)
    academyStaff =  models.ManyToManyField(StaffDB, related_name='project_academyStaff',blank=True)

    salesAmount1 = models.IntegerField(blank=True,null=True)
    salesAmount2 = models.IntegerField(blank=True,null=True)
    salesAmount3 = models.IntegerField(blank=True,null=True)
    salesTotal = models.IntegerField(blank=True,null=True)

    costAmount1 = models.IntegerField(blank=True,null=True)
    costAmount2 = models.IntegerField(blank=True,null=True)
    costAmount3 = models.IntegerField(blank=True,null=True)
    costATotal = models.IntegerField(blank=True,null=True)

    projectcategory = models.ForeignKey(ProjectCategory,on_delete=models.PROTECT, related_name ='project_projectCategory',default=1)    
    projectName = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(max_length=1000,blank=True,null=True)

    projectDateFrom1 = models.DateTimeField(default=timezone.now, blank=True)
    projectDateTo1 = models.DateTimeField(default=timezone.now, blank=True)

    location =models.CharField(max_length=200,blank=True,null=True)

    refURL1 = models.URLField(max_length=2000, blank=True,null=True)
    refURL2 = models.URLField(max_length=2000, blank=True,null=True)
    refURL3 = models.URLField(max_length=2000, blank=True,null=True)

    refFile1 = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)
    refFile2 = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)
    refFile3 = models.FileField(upload_to='files/%Y/%m/%d', blank=True,null=True)

    adminDescription = models.TextField(max_length=300,blank=True,null=True)
    deletedItem = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="Project"

    def __str__(self):
        return   str(self.projectNum)+' '+str(self.client)

