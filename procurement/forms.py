from django import forms
from django.db import models
from django.db.models import Max
import datetime
from django.utils import timezone

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from .models import AdminCheck, DeliveryAddress, ItemCategory, OrderRequest, OrderInfo, Purpose, PaymentMethod, Progress, Supplier, StandardItem
from staffdb.models import StaffDB, Division
from django.forms import ModelForm, inlineformset_factory

from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'


# # 発注・依頼の一括作成

# class AddRequestForm(forms.DateInput):

#     class Meta:
#         model = OrderRequest
#         fields = ('submissionDate',
#             'requestStaffDivision', 'requestStaffdb',
#             'dueDate', 'deliveryAddress', 
#             'costCenter1', 'costCenter2', 'costCenter3',
#             'purpose', 'standardItem', 'requestDetail', 
#             'project','approval', 
#             'quantity', 'estimatedAmount',
#             'refURL1', 'refURL2', 'refURL3',
#             'refFile1','refFile2','refFile3',
#             )
        

# RequestFormset = forms.inlineformset_factory(
#     parent_model = OrderInfo,
#     model = OrderRequest,
#     fields = AddRequestForm,
#     extra=1
#     )

class CreateFormRequest(ModelForm):

    class Meta:
        model  = OrderRequest
        fields = ('submissionDate',
            'requestStaffDivision', 'requestStaffdb',
            'dueDate', 'deliveryAddress', 
            'costCenter1', 'costCenter2', 'costCenter3',
            'purpose', 'standardItem', 'requestDetail', 
            'project','approval', 
            'quantity', 'estimatedAmount',
            'refURL1', 'refURL2', 'refURL3',
            'refFile1','refFile2','refFile3',
            )

        widgets = {'submissionDate': DateInput(),
            'dueDate': DateInput()}

    def __init__(self, *args, **kwargs):
        super(CreateFormRequest, self).__init__(*args, **kwargs)


        # 初期値・入力規則
        today = datetime.date.today()

        self.fields['submissionDate'].initial = today
        self.fields['submissionDate'].widget.attrs['readonly'] = True
  

        self.fields['dueDate'].initial = today + datetime.timedelta(days=5)
        self.fields['dueDate'].required = True
        self.fields['requestStaffdb'].required = True
        self.fields['requestStaffDivision'].required = True
        self.fields['requestStaffDivision'].queryset = Division.objects.filter(no__lt=9000)


        self.fields['deliveryAddress'].required = True

        self.fields['purpose'].required = True
        self.fields['requestDetail'].required = True

        self.fields['quantity'].required = True
        self.fields['estimatedAmount'].required = True
        self.fields['costCenter1'].required = True
        self.fields['costCenter1'].queryset = Division.objects.filter(no__lt=9000)
        self.fields['costCenter2'].queryset = Division.objects.filter(no__lt=9000)
        self.fields['costCenter3'].queryset = Division.objects.filter(no__lt=9000)

        # プレースホルダ
        self.fields['requestDetail'].widget.attrs['placeholder'] = '具体的な商品や要求される仕様（URLを貼っていれば簡潔な説明でOK）'

    def clean(self):
        cleaned_data = super().clean()
        estimatedAmount = cleaned_data.get('estimatedAmount')
        print('A')
        if estimatedAmount == 0 :
            print('B')
            raise forms.ValidationError('金額を入力してください（概算でOK）')


class CreateFormOrder(ModelForm):

    class Meta:
        model = OrderInfo
        fields = ('orderDate',
            'orderStaffdb',
            'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totalAmount', 'paymentMethod', 'orderDescription',
            'settlementDate','refFile',
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
        self.fields['arrivalDate'].initial = today + datetime.timedelta(days=2)

        self.fields['orderStaffdb'].required = True

        self.fields['amount1'].initial = 0
        self.fields['amount2'].initial = 0
        self.fields['amount3'].initial = 0
        self.fields['totalAmount'].initial = 0

        self.fields['amount1'].required = True
        self.fields['amount2'].required = True
        self.fields['amount3'].required = True
        self.fields['totalAmount'].required = True
        self.fields['paymentMethod'].required = True

        # プレースホルダ
        self.fields['irregularSupplier'].widget.attrs['placeholder'] = '標準発注先以外の場合に入力必要'


    def clean(self):
        today = datetime.date.today()
        cleaned_data = super().clean()
        registeredSupplier = cleaned_data.get('registeredSupplier')
        irregularSupplier = cleaned_data.get('irregularSupplier')
        totalAmount = int(cleaned_data.get('totalAmount'))
        registeredSupplier = cleaned_data.get('registeredSupplier')
        paymentMethod = cleaned_data.get('paymentMethod').no
        settlementDate = cleaned_data.get('settlementDate')

        print(registeredSupplier)
        print(paymentMethod)
        print(settlementDate)
        
        if (not irregularSupplier) and (not registeredSupplier):
            raise forms.ValidationError("発注先を入力して下さい")

        elif totalAmount ==0 :
            raise forms.ValidationError("金額を入力して下さい")
        
        elif (not registeredSupplier) and paymentMethod ==1 and ((settlementDate is None) or (settlementDate < today )) :
            raise forms.ValidationError('支払予定日を入力してください（個別発注先・銀行振込の場合）')
        
        else:
            return cleaned_data


class UpdateFormRequest(ModelForm):

    class Meta:
        model  = OrderRequest
        fields = ('requestNum','submissionDate',
            'requestStaffDivision', 'requestStaffdb', 
            'dueDate', 'deliveryAddress', 
            'adminCheck', 'adminStaffdb', 'orderInfo',
            'costCenter1', 'costCenter2', 'costCenter3', 
            'purpose','standardItem', 'requestDetail',
            'project','approval',
            'quantity', 'estimatedAmount',
            'refURL1', 'refURL2', 'refURL3',
            'refFile1', 'refFile2', 'refFile3',
            'adminDescription','deletedItem',
            )
        widgets = {'submissionDate': DateInput(),'dueDate': DateInput()}


    def __init__(self, *args, **kwargs):
        super(UpdateFormRequest, self).__init__(*args, **kwargs)

    # 初期値・入力規則
        self.fields['requestNum'].widget.attrs['readonly'] = True
        self.fields['submissionDate'].widget.attrs['readonly'] = True
        self.fields['requestStaffdb'].required = True
        self.fields['requestStaffDivision'].required = True
        self.fields['requestStaffDivision'].queryset = Division.objects.filter(no__lt=9000)
        self.fields['dueDate'].required = True
        self.fields['deliveryAddress'].required = True
        self.fields['purpose'].required = True
        self.fields['requestDetail'].required = True
        self.fields['costCenter1'].required = True
        self.fields['costCenter1'].queryset = Division.objects.filter(no__lt=9000)
        self.fields['costCenter2'].queryset = Division.objects.filter(no__lt=9000)
        self.fields['costCenter3'].queryset = Division.objects.filter(no__lt=9000)

        self.fields['quantity'].required = True
        self.fields['estimatedAmount'].required = True


        # プレースホルダ
        self.fields['requestDetail'].widget.attrs['placeholder'] = '具体的な商品や要求される仕様（URLを貼っていれば簡潔な説明でOK）'


    def clean(self):
        cleaned_data = super().clean()
        estimatedAmount = cleaned_data.get('estimatedAmount')
        print('A')
        if estimatedAmount == 0 :
            print('B')
            raise forms.ValidationError('金額を入力してください（概算でOK）')




class UpdateFormOrder(ModelForm):

    class Meta:
        model = OrderInfo
        fields = ('orderNum', 'orderDate',
            'progress', 'orderStaffdb',
            'arrivalDate', 
            'registeredSupplier', 'irregularSupplier',
            'amount1', 'amount2', 'amount3', 
            'totalAmount', 'paymentMethod', 'orderDescription',
            'acceptanceDate', 'acceptanceStaffdb',  
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

        self.fields['orderStaffdb'].required = True

        self.fields['amount1'].required = True
        self.fields['amount2'].required = True
        self.fields['amount3'].required = True
        self.fields['totalAmount'].required = True
        self.fields['paymentMethod'].required = True

        # プレースホルダ
        self.fields['irregularSupplier'].widget.attrs['placeholder'] = '標準発注先以外の場合に入力必要'


    def clean(self):
        today = datetime.date.today()
        cleaned_data = super().clean()
        registeredSupplier = cleaned_data.get('registeredSupplier')
        irregularSupplier = cleaned_data.get('irregularSupplier')
        totalAmount = int(cleaned_data.get('totalAmount'))
        registeredSupplier = cleaned_data.get('registeredSupplier')
        paymentMethod = cleaned_data.get('paymentMethod').no
        settlementDate = cleaned_data.get('settlementDate')

        print(registeredSupplier)
        print(paymentMethod)
        print(settlementDate)
        
        if (not irregularSupplier) and (not registeredSupplier):
            raise forms.ValidationError("発注先を入力して下さい")

        elif totalAmount ==0 :
            raise forms.ValidationError("金額を入力して下さい")
        
        elif (not registeredSupplier) and paymentMethod ==1 and ((settlementDate is None) or (settlementDate < today )) :
            raise forms.ValidationError('支払予定日を入力してください（個別発注先・銀行振込の場合）')
        
        else:
            return cleaned_data
