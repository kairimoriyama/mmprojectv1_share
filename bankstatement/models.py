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


class FinancialCategory(models.Model):
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
    accountNumber = models.IntegerField(blank=False,null=False)
    accountType = models.ForeignKey(AccountType,on_delete=models.PROTECT, related_name ='accounttype',blank=True,null=True)
    accountMemo = models.CharField(max_length=50,blank=False,null=False)

    class Meta:
        verbose_name_plural="BankAccount"
        ordering = ('branchName',)

    def __str__(self):
        return self.name


class Statement(models.Model):


    class Meta:
        verbose_name_plural="BankAccount"
        ordering = ('branchName',)

    def __str__(self):
        return self.name
