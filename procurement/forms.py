from django import forms
from django.db.models import Max
import datetime
from django.utils import timezone

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from .models import AdminCheck, Category1, Category2, Division, DeliveryAddress, OrderRequest, OrderInfo, Payment, Progress, Supplier, StandardItem
from django.forms import ModelForm, inlineformset_factory 


class DateInput(forms.DateInput):
    input_type = 'date'


class SelectFormProgress(ModelForm):
    
    progressSelect = forms.ModelChoiceField(
        queryset=Progress.objects,
        required=False
    )     
    class Meta:
        model = Progress
        fields = '__all__'


class SelectFormDivision(ModelForm):
    
    divisionSelect = forms.ModelChoiceField(
        queryset=Division.objects,
        required=False
    )     
    class Meta:
        model = Division
        fields = '__all__'



class CreateFormRequest(ModelForm):

    class Meta:
        model  = OrderRequest
        fields = ('id','requestNum', 'submissionDate',
            'requestStaffDivision', 'requestStaff',
            'adminCheck', 'adminStaff',
            'dueDate', 'deliveryAddress', 
            'costCenter1', 'costCenter2', 'costCenter3', 
            'requestDescription', 'itemCategory1', 'itemCategory2', 
            'standardItem', 'quantity', 
            'estimatedAmount', 'refURL1', 'refURL2', 'refURL3',
            'adminDescription',
            'deletedItem'
            )

        widgets = {'submissionDate': DateInput(),
            'dueDate': DateInput()}

    def __init__(self, *args, **kwargs):
        super(CreateFormRequest, self).__init__(*args, **kwargs)

        
        # requestNumの設定
        currentYear= datetime.date.today().year
        currentYearStr = str(currentYear)
        currentYearRequestNums = OrderRequest.objects.values('requestNum').filter(
            submissionDate__year=currentYear
            )
        lastRequestNum = currentYearRequestNums.aggregate(Max('requestNum'))
        maxRequestNum = lastRequestNum['requestNum__max']

        if (maxRequestNum == None) or (maxRequestNum < 1):
            self.fields['requestNum'].initial = int(currentYearStr[-2:] + "0001")
        else:
            self.fields['requestNum'].initial = maxRequestNum +1 



        # 初期値・入力規則
        today = datetime.date.today()
        self.fields['requestNum'].widget.attrs['readonly'] = True

        self.fields['submissionDate'].initial = datetime.date(
            year=today.year, month=today.month, day=today.day)
        self.fields['submissionDate'].widget.attrs['disabled'] = True

        self.fields['dueDate'].initial = datetime.date(
            year=today.year, month=today.month, day=today.day+5)
        self.fields['dueDate'].required = True
        

        # プレースホルダ


class CreateFormOrder(ModelForm):

    class Meta:
        model = OrderInfo
        fields = ('id','orderNum', 'orderDate',
            'orderRequest', 'progress', 'orderStaff',
            'orderStaffDivision', 'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totlaAmount', 'payment', 'orderDescription', 
            'acceptanceDate', 'acceptanceStaff', 'acceptanceStaffDivision', 
            'acceptanceMemo','deletedItem'
            )
        widgets = {'orderDate': DateInput(), 
            'acceptanceDate': DateInput()}
    
    def __init__(self, *args, **kwargs):
        super(CreateFormOrder, self).__init__(*args, **kwargs)

        # orderNumの設定
        currentYear= datetime.date.today().year
        currentYearStr = str(currentYear)
        currentYearOrderNums = OrderInfo.objects.values('orderNum').filter(
            orderDate__year=currentYear
            )
        lastOrderNum = currentYearOrderNums.aggregate(Max('orderNum'))
        maxOrderNum = lastOrderNum['orderNum__max']

        if (maxOrderNum == None) or (maxOrderNum < 1):
            self.fields['orderNum'].initial = int(currentYearStr[-2:] + "0001")
        else:
            self.fields['orderNum'].initial = maxOrderNum +1 


        # 初期値・入力規則
        self.fields['orderNum'].widget.attrs['readonly'] = 'readonly'

        # プレースホルダ


class UpdateFormRequest(ModelForm):

    class Meta:
        model  = OrderRequest
        fields = ('id','requestNum', 'submissionDate',
            'requestStaffDivision', 'requestStaff', 'adminCheck',
            'dueDate', 'deliveryAddress', 
            'costCenter1', 'costCenter2', 'costCenter3', 
            'requestDescription', 'itemCategory1', 'itemCategory2', 
            'standardItem','quantity', 
            'estimatedAmount', 'refURL1', 'refURL2', 'refURL3',
            'adminDescription',
            'deletedItem'
            )
        widgets = {'submissionDate': DateInput(),
            'dueDate': DateInput()}


    def __init__(self, *args, **kwargs):
        super(ItemUpdateFrom, self).__init__(*args, **kwargs)

        self.fields['requestNum'].widget.attrs['readonly'] = 'readonly'


class UpdateFormOrder(ModelForm):

    class Meta:
        model = OrderInfo
        fields = ('id','orderNum', 'orderDate',
            'orderRequest', 'progress', 'orderStaff',
            'orderStaffDivision', 'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totlaAmount', 'payment', 'orderDescription', 
            'acceptanceDate', 'acceptanceStaff', 'acceptanceStaffDivision', 
            'acceptanceMemo','deletedItem'
            )
        widgets = {'orderDate': DateInput(), 
            'acceptanceDate': DateInput()}


    def __init__(self, *args, **kwargs):
        super(ItemUpdateFrom, self).__init__(*args, **kwargs)

        self.fields['orderNum'].widget.attrs['readonly'] = 'readonly'

