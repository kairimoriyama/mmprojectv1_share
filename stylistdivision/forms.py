from django import forms
from django.db import models

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from .models import ARCheck, ProjectProgress, Client, ProjectCategory, Project
from django.forms import ModelForm, ModelChoiceField

import datetime
from django.utils import timezone



class DateInput(forms.DateInput):
    input_type = 'date'

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


class CreateProjectForm(ModelForm):

    class Meta:
        model  = Project
        fields = (
            'projectProgress',
            'projectPeriodFrom', 'projectPeriodTo', 'projectPeriodDetail', 
            'location',
            'client','clientDetail',
            'projectcategory','projectName',
            'mSatff',
            'staff1', 'staff2','staff3',
            'assistant1','assistant2','assistant3',
            'description',
            'salesAmount1_inctax','salesAmount2_inctax','salesAmount3_inctax','salesAmount2_notax','salesAmount3_notax','salesTotal',
            'costAmount1_inctax','costAmount2_inctax','costAmount3_inctax','costAmount2_notax','costAmount3_notax','costTotal',
            'picture1', 'picture2', 'picture3', 'picture4', 'picture5', 'picture6',
            'refURL1','refURL2','refURL3',
            'refFile1','refFile2','refFile3',
        )
        widgets = {
            'projectPeriodFrom': DateInput(),'projectPeriodTo': DateInput(),   
        }

    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)

        # 初期値・入力規則

        self.fields['projectProgress'].required = True
        self.fields['projectPeriodFrom'].required = True
        self.fields['projectPeriodTo'].required = True
        self.fields['client'].required = True
        self.fields['projectcategory'].required = True
        self.fields['projectName'].required = True
        self.fields['mSatff'].required = True

        # プレースホルダ
        self.fields['projectName'].widget.attrs['placeholder'] = '未定の場合、暫定的なプロジェクトの名前でOK'
        self.fields['description'].widget.attrs['placeholder'] = '案件概要、先方担当者との交渉状況、進捗メモ等'



class UpdateProjectForm(ModelForm):

    class Meta:
        model  = Project
        fields = (
            'projectNum','projectProgress',
            'projectPeriodFrom', 'projectPeriodTo', 'projectPeriodDetail',
            'location',
            'client','clientDetail',
            'projectcategory','projectName',
            'mSatff',
            'staff1', 'staff2','staff3',
            'assistant1','assistant2','assistant3',
            'description',
            'salesAmount1_inctax','salesAmount2_inctax','salesAmount3_inctax','salesAmount2_notax','salesAmount3_notax','salesTotal',
            'costAmount1_inctax','costAmount2_inctax','costAmount3_inctax','costAmount2_notax','costAmount3_notax','costTotal',
            'picture1', 'picture2', 'picture3', 'picture4', 'picture5', 'picture6',
            'refFile1','refFile2','refFile3',
            'refURL1','refURL2','refURL3',

        )
        widgets = {
            'projectPeriodFrom': DateInput(),'projectPeriodTo': DateInput(),   
        }

    def __init__(self, *args, **kwargs):
        super(UpdateProjectForm, self).__init__(*args, **kwargs)

        # 初期値・入力規則
        self.fields['projectNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['projectProgress'].required = True
        self.fields['projectPeriodFrom'].required = True
        self.fields['projectPeriodTo'].required = True
        self.fields['client'].required = True
        self.fields['projectcategory'].required = True
        self.fields['projectName'].required = True
        self.fields['mSatff'].required = True


        # プレースホルダ
        self.fields['projectName'].widget.attrs['placeholder'] = '未定の場合、暫定的なプロジェクトの名前でOK'
        self.fields['description'].widget.attrs['placeholder'] = '案件概要、先方担当者との交渉状況、進捗メモ等'

