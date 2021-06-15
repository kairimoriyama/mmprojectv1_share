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
        ordering = ('branchName',)

    def __str__(self):
        return self.name


class Statement(models.Model):

    no = models.IntegerField(blank=True,null=True)
    recordDate  = models.DateField(default=timezone.now, blank=True)
    paymentAmount = models.IntegerField(default=0,blank=False,null=False)
    deopsitAmount = models.IntegerField(default=0,blank=False,null=False)
    bankAccount = models.ForeignKey(BankAccount,on_delete=models.PROTECT, related_name ='bankaccount',blank=True,null=True)
    journalCategory = models.ForeignKey(JournalCategory,on_delete=models.PROTECT, related_name ='journalcategory',blank=True,null=True)
    bankAccount = models.ForeignKey(BankAccount,on_delete=models.PROTECT, related_name ='bankaccount',blank=True,null=True)
    progress = models.ForeignKey(Progress,on_delete=models.PROTECT, related_name ='progress',blank=True,null=True)


    class Meta:
        verbose_name_plural="BankAccount"
        ordering = ('bankAccount','-id',)

    def __str__(self):
        return self.name
