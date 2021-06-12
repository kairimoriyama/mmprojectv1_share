from django.db import models
from django.utils import timezone
from django.urls import reverse


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
    name = models.CharField(max_length=50,blank=False,null=False)
    accountType = models.ForeignKey(AccountType,on_delete=models.PROTECT, related_name ='accounttype',blank=True,null=True)


    class Meta:
        verbose_name_plural="BankAccount"
        ordering = ('name',)

    def __str__(self):
        return self.name