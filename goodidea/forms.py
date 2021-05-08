from django import forms
from django.db.models import Max
import datetime
from django.utils import timezone

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from .models import Item, Progress, Division, Category, Image
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


class ModelFormWithFormSetMixin:

    def __init__(self, *args, **kwargs):
        super(ModelFormWithFormSetMixin, self).__init__(*args, **kwargs)
        self.formset = self.formset_class(
            instance=self.instance,
            data=self.data if self.is_bound else None,
        )

    def is_valid(self):
        return super(ModelFormWithFormSetMixin, self).is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        saved_instance = super(ModelFormWithFormSetMixin, self).save(commit)
        self.formset.save(commit)
        return saved_instance

class ImageUploadForm(ModelForm):

    class Meta:
        model = Image
        fields= ('picture',)

ImageFormset = inlineformset_factory(
    parent_model=Item,
    model=Image,
    form=ImageUploadForm,
    extra=6
)

class ItemCreateFromIdea(ModelFormWithFormSetMixin, ModelForm):

    formset_class = ImageFormset

    class Meta:
        model  = Item
        fields = ('itemNum','ideaNum','submissionDate','progress','division','staff','category','system','purchase','title','description','refURL1','refURL2','refURL3','refFile1','refFile2','refFile3','inchargeDivision','inchargeStaff' )
        widgets = {'submissionDate': DateInput()}

    def __init__(self, *args, **kwargs):
        super(ItemCreateFromIdea, self).__init__(*args, **kwargs)

        
        # ideaNumの設定
        currentYear= datetime.date.today().year
        currentYearStr = str(currentYear)
        currentYearIdeaNums = Item.objects.values('ideaNum').filter(
            submissionDate__year=currentYear
            )
        lastIdeaNum = currentYearIdeaNums.aggregate(Max('ideaNum'))
        maxIdeaNum = lastIdeaNum['ideaNum__max']

        if (maxIdeaNum == None) or (maxIdeaNum < 1):
            self.fields['ideaNum'].initial = int(currentYearStr[-2:] + "0001")
        else:
            self.fields['ideaNum'].initial = maxIdeaNum +1 

        # itemNumの設定
        ItemNums = Item.objects.values('itemNum')
        lastItemNum = ItemNums.aggregate(Max('itemNum'))
        maxItemNum = lastItemNum['itemNum__max']

        if (maxItemNum == None) or (maxItemNum < 1):
            self.fields['itemNum'].initial = 1
        else:
            self.fields['itemNum'].initial = maxItemNum +1 


        # 初期値・入力規則
        self.fields['itemNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['ideaNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['progress'].initial = 1
        self.fields['staff'].required = True
        self.fields['division'].required = True
        self.fields['category'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True

        # プレースホルダ
        self.fields['inchargeStaff'].widget.attrs['placeholder'] = '事前に決めていれば'
        self.fields['inchargeDivision'].widget.attrs['placeholder'] = '事前に決めていれば'
        self.fields['title'].widget.attrs['placeholder'] = 'できるだけ具体的に業務フローの変更点、備品の発注先・金額等を記載（必要に応じてURL・写真・資料を追加）'
        self.fields['description'].widget.attrs['placeholder'] = '現状の分析に基づく課題提起、複数の代替案との比較、費用対効果の検証等を記載（必要に応じてURL・写真・資料を追加）'



class ItemCreateFromAction(ModelFormWithFormSetMixin, ModelForm):

    formset_class = ImageFormset

    class Meta:
        model  = Item
        fields = ('itemNum','actionNum','submissionDate','progress','division','staff','category','system','purchase','title','description','refURL1','refURL2','refURL3','refFile1','refFile2','refFile3','inchargeDivision','inchargeStaff', 'completionDate' )
        widgets = {'submissionDate': DateInput(), 'completionDate': DateInput()}
    
    def __init__(self, *args, **kwargs):
        super(ItemCreateFromAction, self).__init__(*args, **kwargs)

        # actionNumの設定
        currentYear= datetime.date.today().year
        currentYearStr = str(currentYear)
        currentYearActionNums = Item.objects.values('actionNum').filter(
            submissionDate__year=currentYear
            )
        lastActionNum = currentYearActionNums.aggregate(Max('actionNum'))
        maxActionNum = lastActionNum['actionNum__max']

        print(maxActionNum)

        if (maxActionNum == None) or (maxActionNum < 1):
            self.fields['actionNum'].initial = int(currentYearStr[-2:] + "001")
        else:
            self.fields['actionNum'].initial = maxActionNum +1 


        # itemNumの設定
        
        ItemNums = Item.objects.values('itemNum')
        lastItemNum = ItemNums.aggregate(Max('itemNum'))
        maxItemNum = lastItemNum['itemNum__max']

        if (maxItemNum == None) or (maxItemNum < 1):
            self.fields['itemNum'].initial = 1
        else:
            self.fields['itemNum'].initial = maxItemNum +1 

        # 初期値・入力規則
        self.fields['itemNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['actionNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['progress'].initial = 4
        self.fields['completionDate'].required = True
        self.fields['staff'].required = True
        self.fields['division'].required = True
        self.fields['category'].required = True
        self.fields['inchargeStaff'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True

        # プレースホルダ
        self.fields['inchargeStaff'].widget.attrs['placeholder'] = '協力者含む'
        self.fields['inchargeDivision'].widget.attrs['placeholder'] = '協力部門含む'
        self.fields['title'].widget.attrs['placeholder'] = 'できるだけ具体的に業務フローの変更点、備品の発注先・金額等を記載（必要に応じてURL・写真・資料を追加）'
        self.fields['description'].widget.attrs['placeholder'] = '現状の分析に基づく課題提起、複数の代替案との比較、費用対効果の検証等を記載（必要に応じてURL・写真・資料を追加）'



class ItemUpdateFrom(ModelFormWithFormSetMixin, ModelForm):

    formset_class = ImageFormset

    class Meta:
        model  = Item
        fields = ('itemNum','ideaNum','actionNum','submissionDate','progress','division','staff','category','system','purchase','title','description','refURL1','refURL2','refURL3','refFile1','refFile2','refFile3','discussionDate','discussionNote','report','inchargeDivision','inchargeStaff','completionDate','dueDate','adminMemo','deletedItem')

        widgets = { 'discussionDate': DateInput(), 'completionDate': DateInput(), 'dueDate': DateInput()}
    
    def __init__(self, *args, **kwargs):
        super(ItemUpdateFrom, self).__init__(*args, **kwargs)

        self.fields['itemNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['ideaNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['actionNum'].widget.attrs['readonly'] = 'readonly'
        self.fields['progress'].required = True
        self.fields['division'].required = True
        self.fields['staff'].required = True
        self.fields['category'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True

