from django import forms
from django.db import models
from django.db.models import Max
import datetime
from django.utils import timezone

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from .models import AdminCheck, Category1, Category2, Division, DeliveryAddress, OrderRequest, OrderInfo, Payment, Progress, Supplier, StandardItem
from django.forms import ModelForm, inlineformset_factory 


# 検収用フォーム 使いたいが使えていない
class AcceptanceForm(forms.Form):
    progress = models.ForeignKey(Progress,on_delete=models.PROTECT, related_name ='orderInfo_adminCheck',default=1)    
    acceptanceDate = models.DateField(blank=True,null=True)
    acceptanceStaff = models.CharField(max_length=20,blank=True,null=True)
    acceptanceStaffDivision = models.ForeignKey(Division,on_delete=models.PROTECT, related_name ='orderRequest_acceptanceStaff',blank=True,null=True) 
    acceptanceMemo = models.TextField(max_length=100,blank=True,null=True)

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
        fields = ('submissionDate',
            'requestStaffDivision', 'requestStaff',
            'dueDate', 'deliveryAddress', 
            'costCenter1', 'costCenter2', 'costCenter3', 
            'requestDescription', 'project','approved',
            'itemCategory1', 'itemCategory2', 
            'standardItem', 'quantity', 
            'estimatedAmount', 'refURL1', 'refURL2', 'refURL3',
            'refFile'
            )

        widgets = {'submissionDate': DateInput(),
            'dueDate': DateInput()}

    def __init__(self, *args, **kwargs):
        super(CreateFormRequest, self).__init__(*args, **kwargs)


        # 初期値・入力規則
        today = datetime.date.today()

        self.fields['submissionDate'].initial = today
        self.fields['submissionDate'].widget.attrs['readonly'] = True

        self.fields['requestStaff'].required = True
        self.fields['requestStaffDivision'].required = True

        self.fields['dueDate'].initial = today
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


        # プレースホルダ
        self.fields['requestDescription'].widget.attrs['placeholder'] = '標準品以外の依頼の場合、依頼目的と商品の要件を記入'




class CreateFormOrder(ModelForm):

    class Meta:
        model = OrderInfo
        fields = ('orderDate',
            'orderStaff',
            'orderStaffDivision', 'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totalAmount', 'payment', 'orderDescription',
            'settlementDate',
            )
        widgets = {'orderDate': DateInput(),
                   'arrivalDate': DateInput(),
                   'settlementDate': DateInput()}
    
    def __init__(self, *args, **kwargs):
        super(CreateFormOrder, self).__init__(*args, **kwargs)

        

        # 初期値・入力規則
        today = datetime.date.today()
        self.fields['orderDate'].required = True
        self.fields['orderDate'].initial = today
        self.fields['orderDate'].widget.attrs['readonly'] = True
               
        self.fields['arrivalDate'].required = True
        self.fields['arrivalDate'].initial = today

        self.fields['orderStaff'].required = True
        self.fields['orderStaffDivision'].required = True

        self.fields['amount1'].initial = 0
        self.fields['amount2'].initial = 0
        self.fields['amount3'].initial = 0
        self.fields['totalAmount'].initial = 0

        self.fields['amount1'].required = True
        self.fields['amount2'].required = True
        self.fields['amount3'].required = True
        self.fields['totalAmount'].required = True
        self.fields['payment'].required = True

        # プレースホルダ
        self.fields['irregularSupplier'].widget.attrs['placeholder'] = '標準発注先以外の場合に入力必要'



class UpdateFormRequest(ModelForm):

    class Meta:
        model  = OrderRequest
        fields = ('requestNum','submissionDate',
            'requestStaffDivision', 'requestStaff', 
            'dueDate', 'deliveryAddress', 
            'adminCheck', 'adminStaff', 'orderInfo',
            'costCenter1', 'costCenter2', 'costCenter3', 
            'requestDescription', 'project','approved',
            'itemCategory1', 'itemCategory2', 
            'standardItem','quantity', 
            'estimatedAmount', 'refURL1', 'refURL2', 'refURL3',
            'adminDescription','refFile',
            'deletedItem',
            )
        widgets = {'submissionDate': DateInput(),'dueDate': DateInput()}


    def __init__(self, *args, **kwargs):
        super(UpdateFormRequest, self).__init__(*args, **kwargs)

    # 初期値・入力規則
        self.fields['requestNum'].widget.attrs['readonly'] = True
        self.fields['submissionDate'].widget.attrs['readonly'] = True
        self.fields['requestStaff'].required = True
        self.fields['requestStaffDivision'].required = True
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

    
        # プレースホルダ
        self.fields['requestDescription'].widget.attrs['placeholder'] = '標準品以外の依頼の場合、依頼目的と商品の要件を記入'



class UpdateFormOrder(ModelForm):

    class Meta:
        model = OrderInfo
        fields = ('orderNum', 'orderDate',
            'progress', 'orderStaff',
            'orderStaffDivision', 'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totalAmount', 'payment', 'orderDescription',
            'acceptanceDate', 'acceptanceStaff', 'acceptanceStaffDivision', 
            'acceptanceMemo',
            'settlementDate','settlement','refFile',
            'deletedItem'
            )
        widgets = {'orderDate': DateInput(),
            'arrivalDate': DateInput(),
            'acceptanceDate': DateInput(),
            'settlementDate': DateInput()}


    def __init__(self, *args, **kwargs):
        super(UpdateFormOrder, self).__init__(*args, **kwargs)


        # 初期値・入力規則
        self.fields['orderNum'].widget.attrs['readonly'] = True
        self.fields['progress'].required = True

        self.fields['orderDate'].required = True
        
        self.fields['arrivalDate'].required = True

        self.fields['orderStaff'].required = True
        self.fields['orderStaffDivision'].required = True

        self.fields['amount1'].required = True
        self.fields['amount2'].required = True
        self.fields['amount3'].required = True
        self.fields['totalAmount'].required = True
        self.fields['payment'].required = True

        # プレースホルダ
        self.fields['irregularSupplier'].widget.attrs['placeholder'] = '標準発注先以外の場合に入力必要'


