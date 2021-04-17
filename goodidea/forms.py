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
        fields = ('itemNum','ideaNum','submissionDate','progress','division','staff','category','title','description','refURL1','refURL2','refURL3','picture1','picture2','picture3','refFile1','refFile2','refFile3', )
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
        self.fields['title'].required = True
        self.fields['description'].required = True



class ItemCreateFromAction(ModelForm):

    class Meta:
        model  = Item
        fields = ('itemNum','actionNum','submissionDate','progress','division','staff','category','title','description','refURL1','refURL2','refURL3','picture1','picture2','picture3','refFile1','refFile2','refFile3', 'completionDate' )
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
        self.fields['title'].required = True
        self.fields['description'].required = True



class ItemUpdateFrom(ModelForm):

    class Meta:
        model  = Item
<<<<<<< HEAD
        fields = ('itemNum','ideaNum','actionNum','submissionDate','progress','division','staff','category','title','description','refURL1','refURL2','refURL3','picture1','picture2','picture3','refFile1','refFile2','refFile3','discussionDate','discussionNote','report','inchargeDivision','inchargeStaff','completionDate','dueDate','adminMemo','deletedItem')

        widgets = { 'discussionDate': DateInput(), 'completionDate': DateInput(), 'dueDate': DateInput()}
=======
        fields = ('itemNum','ideaNum','actionNum','submissionDate','progress','division','staff','category','title','description','refURL1','refURL2','refURL3','picture1','picture2','picture3','refFile1','refFile2','refFile3','discussionDate','discussionNote','report','inchargeDivision','inchargeStaff','completionDate','adminMemo','deletedItem')

        widgets = { 'discussionDate': DateInput(), 'completionDate': DateInput()}
>>>>>>> origin/main
    
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

