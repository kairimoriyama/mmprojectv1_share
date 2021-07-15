from django import forms
from django.db import models

from .models import ARCheck, ProjectProgress, Client, ProjectCategory
from django.forms import ModelForm, ModelChoiceField


class SettlementFilterForm(forms.Form):
    arCheck = forms.ModelChoiceField(
        label='明細確認状況',
        required=False,
        queryset=ARCheck.objects.order_by('no'),
        widget=forms.Select,
    )


class ProjectFilterForm(forms.Form):

    projectProgress = forms.ModelChoiceField(
        label='プロジェクト進捗',
        required=False,
        queryset=ProjectProgress.objects.order_by('no'),
        widget=forms.Select,
    )

    client = forms.ModelChoiceField(
        label='顧客',
        required=False,
        queryset=Client.objects.order_by('no'),
        widget=forms.Select,
    )

    projectCategory = forms.ModelChoiceField(
        label='案件区分',
        required=False,
        queryset=ProjectCategory.objects.order_by('no'),
        widget=forms.Select,
    )



