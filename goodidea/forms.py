from django import forms
from django.db.models import Max
import datetime
from django.utils import timezone

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from .models import Item, Progress, Division, Category
from django.forms import ModelForm, inlineformset_factory 


class DateInput(forms.DateInput):
    input_type = 'date'


class ProgressSelectForm(ModelForm):
    
    progressSelect = forms.ModelChoiceField(
        queryset=Progress.objects,
        required=False
    )     
    class Meta:
        model = Progress
        fields = '__all__'


class DivisionSelectForm(ModelForm):
    
    divisionSelect = forms.ModelChoiceField(
        queryset=Division.objects,
        required=False
    )     
    class Meta:
        model = Division
        fields = '__all__'



class ItemCreateFromIdea(ModelForm):

    class Meta:
        model  = Item
        fields = ('submissionDate','progress','division','staff','staffdb',
        'category','system','purchase','title','description',
        'refURL1','refURL2','refURL3',
        'picture1','picture2','picture3','picture4','picture5','picture6',
        'refFile1','refFile2','refFile3','inchargeDivision','inchargeStaff' )
        widgets = {'submissionDate': DateInput()}

    def __init__(self, *args, **kwargs):
        super(ItemCreateFromIdea, self).__init__(*args, **kwargs)

        # 初期値・入力規則
        self.fields['progress'].initial = 1
        self.fields['staffdb'].required = True
        self.fields['division'].required = True
        self.fields['category'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True

        # プレースホルダ
        self.fields['inchargeStaff'].widget.attrs['placeholder'] = '事前に決めていれば'
        self.fields['inchargeDivision'].widget.attrs['placeholder'] = '事前に決めていれば'
        self.fields['title'].widget.attrs['placeholder'] = 'できるだけ具体的に業務フローの変更点、備品の発注先・金額等を記載（必要に応じてURL・写真・資料を追加）'
        self.fields['description'].widget.attrs['placeholder'] = '現状の分析に基づく課題提起、複数の代替案との比較、費用対効果の検証等を記載（必要に応じてURL・写真・資料を追加）'



class ItemCreateFromAction(ModelForm):

    class Meta:
        model  = Item
        fields = ('submissionDate','progress','division','staffdb','category',
        'system','purchase','title','description',
        'refURL1','refURL2','refURL3',
        'picture1','picture2','picture3','picture4','picture5','picture6',
        'refFile1','refFile2','refFile3',
        'inchargeDivision','inchargeStaff', 'completionDate' )
        widgets = {'submissionDate': DateInput(), 'completionDate': DateInput()}
    
    def __init__(self, *args, **kwargs):
        super(ItemCreateFromAction, self).__init__(*args, **kwargs)

        
        # 初期値・入力規則
        today = datetime.date.today()

        self.fields['progress'].initial = 4
        self.fields['completionDate'].initial = today
        self.fields['completionDate'].required = True
        self.fields['staffdb'].required = True
        self.fields['division'].required = True
        self.fields['category'].required = True
        self.fields['inchargeStaff'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True

        # プレースホルダ
        self.fields['inchargeStaff'].widget.attrs['placeholder'] = '協力者含む'
        self.fields['inchargeDivision'].widget.attrs['placeholder'] = '協力部門含む'
        self.fields['title'].widget.attrs['placeholder'] = 'できるだけ具体的に業務フローの変更点、備品の発注先・金額等を記載（必要に応じてURL・写真・資料を追加）'
        self.fields['description'].widget.attrs['placeholder'] = '現状・分析・対策（必要に応じてURL・写真・資料を追加）'



class ItemUpdateFrom(ModelForm):

    class Meta:
        model  = Item
        fields = ('ideaNum','actionNum','submissionDate','progress','division','staffdb',
        'category','system','purchase','title','description',
        'refURL1','refURL2','refURL3',
        'picture1','picture2','picture3','picture4','picture5','picture6',
        'refFile1','refFile2','refFile3',
        'discussionDate','discussionNote','report','inchargeDivision','inchargeStaff', 'internalDiscussion',
        'completionDate','dueDate','adminMemo','deletedItem')

        widgets = { 'discussionDate': DateInput(), 'completionDate': DateInput(), 'dueDate': DateInput()}
    
    def __init__(self, *args, **kwargs):
        super(ItemUpdateFrom, self).__init__(*args, **kwargs)

        self.fields['ideaNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['actionNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['progress'].required = True
        self.fields['division'].required = True
        self.fields['staffdb'].required = True
        self.fields['category'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True