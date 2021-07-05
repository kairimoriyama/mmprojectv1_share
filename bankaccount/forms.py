from django import forms
from django.db import models

from .models import BankAccount, JournalCategory
from staffdb.models import StaffDB, Division
from django.forms import ModelForm, ModelChoiceField


class SearchForm(forms.Form):
    bankAccount = forms.ModelChoiceField(
        label='銀行口座',
        required=False,
        queryset=BankAccount.objects.order_by('no'),
        widget=forms.Select,
    )
    journalCategory = forms.ModelChoiceField(
        label='会計区分',
        required=False,
        queryset=JournalCategory.objects.order_by('no'),
        widget=forms.Select,
    )

