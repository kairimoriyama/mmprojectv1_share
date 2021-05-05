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
        fields = ('requestNum', 'submissionDate',
            'requestStaffDivision', 'requestStaff',
            'dueDate', 'deliveryAddress', 
            'costCenter1', 'costCenter2', 'costCenter3', 
            'requestDescription', 'itemCategory1', 'itemCategory2', 
            'standardItem', 'quantity', 
            'estimatedAmount', 'refURL1', 'refURL2', 'refURL3',
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

        self.fields['submissionDate'].initial = today
        self.fields['submissionDate'].widget.attrs['readonly'] = True

        self.fields['requestStaff'].required = True
        self.fields['requestStaffDivision'].required = True

        self.fields['dueDate'].initial = datetime.date(
            year=today.year, month=today.month, day=today.day+5)
        self.fields['dueDate'].required = True
        self.fields['deliveryAddress'].required = True
        self.fields['itemCategory1'].required = True
        self.fields['itemCategory2'].required = True
        self.fields['costCenter1'].required = True

        # if self.fields['itemCategory2'] :
        #     self.fields['requestDescription'].required = True
        # else:
        #     self.fields['itemCategory2'].required = True

        self.fields['quantity'].required = True
        self.fields['estimatedAmount'].required = True

        print("requestNum")

        # プレースホルダ
        self.fields['requestDescription'].widget.attrs['placeholder'] = '標準品以外の依頼の場合、依頼目的と商品の要件を記入'




class CreateFormOrder(ModelForm):

    class Meta:
        model = OrderInfo
        fields = ('orderNum', 'orderDate',
            'progress', 'orderStaff',
            'orderStaffDivision', 'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totalAmount', 'payment', 'orderDescription',
            )
        widgets = {'orderDate': DateInput()}
    
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
        self.fields['orderNum'].widget.attrs['readonly'] = True
        self.fields['progress'].widget.attrs['readonly'] = True

        # プレースホルダ


class UpdateFormRequest(ModelForm):

    class Meta:
        model  = OrderRequest
        fields = ('requestStaffDivision', 'requestStaff', 
            'dueDate', 'deliveryAddress', 
            'adminCheck', 'adminStaff', 'orderInfo',
            'costCenter1', 'costCenter2', 'costCenter3', 
            'requestDescription', 'itemCategory1', 'itemCategory2', 
            'standardItem','quantity', 
            'estimatedAmount', 'refURL1', 'refURL2', 'refURL3',
            'adminDescription',
            'deletedItem'
            )
        widgets = {'dueDate': DateInput()}


    def __init__(self, *args, **kwargs):
        super(UpdateFormRequest, self).__init__(*args, **kwargs)

    

class UpdateFormOrder(ModelForm):

    class Meta:
        model = OrderInfo
        fields = ('progress', 'orderStaff',
            'orderStaffDivision', 'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totalAmount', 'payment', 'orderDescription', 
            'acceptanceDate', 'acceptanceStaff', 'acceptanceStaffDivision', 
            'acceptanceMemo','deletedItem'
            )
        widgets = {'orderDate': DateInput(),
            'arrivalDate': DateInput(),
            'acceptanceDate': DateInput()}


    def __init__(self, *args, **kwargs):
        super(UpdateFormOrder, self).__init__(*args, **kwargs)

