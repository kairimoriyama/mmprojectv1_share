from django.db import models
from django.utils import timezone
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class Division(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    def __str__(self):
        return self.name

class DeliveryAddress(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="DeliveryAddress"

    def __str__(self):
        return self.name


class AdminCheck(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="AdminCheck"

    def __str__(self):
        return self.name

class Category1(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="Category1"

    def __str__(self):
        return self.name

class Category2(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)
    category1 = models.ForeignKey(Category1,on_delete=models.PROTECT, related_name ='category2_category1',blank=True,null=True)

    class Meta:
        verbose_name_plural="Category2"

    def __str__(self):
        return self.name

class Progress(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="Progress"

    def __str__(self):
        return self.name


class Payment(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="Payment"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)
    tel = models.CharField(max_length=20, blank=True,null=True)
    email = models.EmailField(max_length=50, blank=True,null=True)
    webpageURL = models.URLField(max_length=300, blank=True,null=True)
    commonId = models.CharField(max_length=20, blank=True,null=True)
    commonPass = models.CharField(max_length=20, blank=True,null=True)
    description = models.TextField(max_length=200, blank=True,null=True)

    class Meta:
        verbose_name_plural="Supplier"

    def __str__(self):
        return self.name


class StandardItem(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)
    category2 = models.ForeignKey(Category2,on_delete=models.PROTECT, related_name ='standardItem_category2',blank=True,null=True)
    description = models.TextField(max_length=400, blank=True,null=True)
    price = models.IntegerField(blank=True,null=True)
    picture1 = models.ImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)
    picture2 = models.ImageField(upload_to='images/%Y/%m/%d', blank=True,null=True)
    refURL1 = models.URLField(max_length=300, blank=True,null=True)
    refURL2 = models.URLField(max_length=300, blank=True,null=True)
    supplier = models.ForeignKey(Supplier,on_delete=models.PROTECT, related_name ='standardItem_supplier',blank=True,null=True)

    class Meta:
        verbose_name_plural="StandardItem"

    def __str__(self):
        return self.name



class OrderInfo(models.Model):
    orderNum =  models.IntegerField(blank=False,null=False)
    orderDate = models.DateField(default=timezone.now, blank=True)
    
    progress = models.ForeignKey(Progress,on_delete=models.PROTECT, related_name ='orderInfo_adminCheck',default=1)    
    orderStaff = models.CharField(max_length=20,blank=True,null=True)
    orderStaffDivision = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='orderInfo_orderStafDividion',blank=True,null=True) 

    registeredSupplier = models.ForeignKey(Supplier,on_delete=models.PROTECT, related_name ='orderInfo_supplier',blank=True,null=True) 
    irregularSupplier = models.CharField(max_length=100,blank=True,null=True)
    
    arrivalDate = models.DateField(default=timezone.now, blank=True)
    amount1 = models.IntegerField(blank=True,null=True)
    amount2 = models.IntegerField(blank=True,null=True)
    amount3 = models.IntegerField(blank=True,null=True)
    totalAmount = models.IntegerField(blank=True,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.PROTECT, related_name ='orderInfo_payment',blank=True,null=True)    
    orderDescription = models.TextField(max_length=50,blank=True,null=True)

    acceptanceDate = models.DateField(blank=True,null=True)
    acceptanceStaff = models.CharField(max_length=20,blank=True,null=True)
    acceptanceStaffDivision = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='orderRequest_acceptanceStaff',blank=True,null=True) 
    acceptanceMemo = models.TextField(max_length=100,blank=True,null=True)

    settlementDate = models.DateField(blank=True,null=True)
    settlement = models.BooleanField(default=False)

    deletedItem = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="OrderInfo"

    def __str__(self):
        return str(self.orderNum) + ' ' +  str(self.orderDate)



class OrderRequest(models.Model):
    requestNum =  models.IntegerField(blank=False,null=False)
    submissionDate = models.DateField(default=timezone.now, blank=True)
    orderInfo = models.ForeignKey(OrderInfo,on_delete=models.PROTECT, related_name ='orderRequest_orderInfo',blank=True,null=True) 

    requestStaffDivision = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='orderRequest_dividion') 
    requestStaff = models.CharField(max_length=20)

    adminCheck = models.ForeignKey(AdminCheck,on_delete=models.PROTECT, related_name ='orderRequest_adminCheck',default=1)    
    adminStaff = models.CharField(max_length=20,blank=True,null=True)
    
    
    dueDate = models.DateField(default=timezone.now, blank=True)
    deliveryAddress = models.ForeignKey(DeliveryAddress,on_delete=models.PROTECT, related_name ='orderRequest_deliveryAddress') 
 
    costCenter1 = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='orderRequest_cost1_dividion',blank=True,null=True) 
    costCenter2 = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='orderRequest_cost2_dividion',blank=True,null=True) 
    costCenter3 = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='orderRequest_cost3_dividion',blank=True,null=True) 

    itemCategory1 = models.ForeignKey(Category1,on_delete=models.PROTECT, related_name ='orderRequest_category1',blank=True,null=True) 
    itemCategory2 = models.ForeignKey(Category2,on_delete=models.PROTECT, related_name ='orderRequest_category2',blank=True,null=True) 
    standardItem = models.ForeignKey(StandardItem,on_delete=models.PROTECT, related_name ='orderRequest_standardItem',blank=True,null=True) 
    requestDescription = models.TextField(max_length=400,blank=True,null=True)

    project = models.CharField(max_length=30,blank=True,null=True)
    approved = models.CharField(max_length=30,blank=True,null=True)

    quantity = models.CharField(max_length=100)
    estimatedAmount = models.IntegerField(blank=True,null=True)

    refURL1 = models.URLField(max_length=300, blank=True,null=True)
    refURL2 = models.URLField(max_length=300, blank=True,null=True)
    refURL3 = models.URLField(max_length=300, blank=True,null=True)

    adminDescription = models.TextField(max_length=300,blank=True,null=True)
    deletedItem = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural="OrderRequest"

    def __str__(self):
        return   str(self.requestNum)+' '+self.requestStaff

