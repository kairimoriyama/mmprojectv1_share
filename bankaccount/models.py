from django.db import models
from django.utils import timezone
from django.urls import reverse



class Progress(models.Model):
    no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=50)
    
    class Meta:
        ordering = ('no',)

    def __str__(self):
        return self.name


class JournalCategory(models.Model):
    no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=50)
    
    class Meta:
        ordering = ('no',)

    def __str__(self):
        return self.name


class AccountType(models.Model):
    no = models.IntegerField(blank=False,null=False)
    name = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="AccountType"
        ordering = ('no',)

    def __str__(self):
        return self.name

class BankAccount(models.Model):
    no = models.IntegerField(blank=False,null=False)
    branchName = models.CharField(max_length=50,blank=False,null=False)
    accountNumber = models.IntegerField(blank=True,null=True)
    accountType = models.ForeignKey(AccountType,on_delete=models.PROTECT, related_name ='accounttype',blank=True,null=True)
    accountMemo = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        verbose_name_plural="BankAccount"
        ordering = ('no',)

    def __str__(self):
        return self.branchName + str(self.accountNumber)


class Statement(models.Model):

    no = models.IntegerField(blank=True,null=True)
    transactionDate  = models.DateField(default=timezone.now, blank=True,null=True)

    bankAccount = models.ForeignKey(BankAccount,on_delete=models.PROTECT, related_name ='bankaccount',blank=True,null=True)
    dateDescription  = models.CharField(max_length=20,blank=True,null=True)
    
    description1 = models.CharField(max_length=10,blank=True,null=True)
    description2 = models.CharField(max_length=30,blank=True,null=True)
    paymentAmount = models.IntegerField(default=0,blank=False,null=False)
    deopsitAmount = models.IntegerField(default=0,blank=False,null=False)
    accountBalance = models.IntegerField(default=0,blank=False,null=False)
    
    journalCategory = models.ForeignKey(JournalCategory,on_delete=models.PROTECT, related_name ='journalcategory',blank=True,null=True)
   
    progress = models.ForeignKey(Progress,on_delete=models.PROTECT, related_name ='progress',blank=True,null=True)
    consistencyCheck = models.BooleanField(default=False)
    adminMemo = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        verbose_name_plural="Statement"
        ordering = ('-no',)

    def __str__(self):
        return str(self.deopsitAmount)+'-'+str(self.paymentAmount)+'-'+str(self.accountBalance)
