from django import forms
from django.db import models

from .models import ARCheck
from django.forms import ModelForm, ModelChoiceField


class SelectForm(forms.Form):
    arCheck = forms.ModelChoiceField(
        label='明細確認状況',
        required=False,
        queryset=ARCheck.objects.order_by('no'),
        widget=forms.Select,
    )


