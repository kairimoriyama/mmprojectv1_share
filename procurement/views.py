from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q, Max
from django.core import validators
import unicodecsv as csv
from django.contrib import messages


import datetime
from django.utils import timezone

from .models import AdminCheck, Category1, Category2, Division, DeliveryAddress, OrderRequest, OrderInfo, Payment, Progress, Supplier, StandardItem
from .forms import  CreateFormRequest, CreateFormOrder, UpdateFormRequest ,UpdateFormOrder, AcceptanceForm

# Create your views here.


class ListALL(ListView):
    template_name = 'procurement/list_all.html'
    model  = OrderRequest
    fields = '__all__'
    queryset = OrderRequest.objects.filter(deletedItem=False
    ).order_by('-id').order_by('adminCheck__no').exclude(adminCheck__gte=5)

    def get_context_data(self, **kwargs):
        context = super(ListALL, self).get_context_data(**kwargs)
        context.update({
            'object_list_order': OrderInfo.objects.exclude(progress__gte=3),
        })

        context['divisionSelect_list'] = Division.objects.all()

        return context
    
    # 検収・発注報告をPOSTメソッドにより実施
    def post(self, request, *args, **kwargs):
       
        # 検収入力フォーム

        if request.method == 'POST':
            if 'button_acceptance' in request.POST:

                # HTMLから取得した値
                acceptanceStaff = self.request.POST.get('staff_acceptance')
                acceptanceStaffDivision = self.request.POST.get('division_acceptance')
                acceptanceDate = self.request.POST.get('acceptanceDate_acceptance')
                acceptanceMemo = self.request.POST.get('acceptanceMemo_acceptance')
                selected_order_pk_acceptance = self.request.POST.get('selected_order_pk_acceptance')

                # リスト型
                selected_request_pk_acceptance = []
                # カンマ区切りでリスト型へ
                selected_request_pk_acceptance = self.request.POST.get('selected_request_pk_acceptance').split(sep=',')

                print(selected_request_pk_acceptance)
                print(selected_order_pk_acceptance)


                if acceptanceStaff is None or  acceptanceStaff == "" or acceptanceStaffDivision is None or acceptanceDate is None:
                    pass

                else:
                    # 注文の検収情報を更新
                    orderInfoAcceptance = get_object_or_404(OrderInfo, pk=selected_order_pk_acceptance)
                    orderInfoAcceptance.acceptanceStaff = acceptanceStaff
                    
                    # Foreignkey Division
                    divisionAcceptance = get_object_or_404(Division, pk=acceptanceStaffDivision)
                    orderInfoAcceptance.acceptanceStaffDivision = divisionAcceptance

                    orderInfoAcceptance.acceptanceDate = acceptanceDate
                    orderInfoAcceptance.acceptanceMemo = acceptanceMemo

                    # Foreignkey Progress
                    progressAcceptance = get_object_or_404(Progress, pk=3)
                    orderInfoAcceptance.progress = progressAcceptance

                    # 発注情報の更新を保存
                    orderInfoAcceptance.save()

                    # 依頼を検収済みに更新
                    for acceptance_request_pk in selected_request_pk_acceptance:
                        print(acceptance_request_pk)
                        orderRequestAcceptance = get_object_or_404(OrderRequest, pk=acceptance_request_pk)
                        adminCheckAcceptance = get_object_or_404(AdminCheck, pk=5)
                        # リストで全件更新
                        orderRequestAcceptance.adminCheck = adminCheckAcceptance 
                        orderRequestAcceptance.save()
                                        
                    print('Successfully updated!')

                return self.get(request, *args, **kwargs)

            if 'button_report_order' in request.POST:

                print('発注報告')

            return self.get(request, *args, **kwargs)

        else:
            pass

        



class ListRequest(ListView):
    template_name = 'procurement/list_request.html'
    model  = OrderRequest
    fields = '__all__'
    queryset = OrderRequest.objects.filter(deletedItem=False
    ).order_by('-id').order_by('adminCheck__no')
    paginate_by = 22

class ListOrder(ListView):
    template_name = 'procurement/list_order.html'
    model  = OrderInfo
    fields = '__all__'
    queryset = OrderInfo.objects.filter(deletedItem=False).order_by('-id')
    paginate_by = 22




class DetailRequest(DetailView):
    template_name = 'procurement/detail_request.html'
    model  = OrderRequest
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orderRequest = self.object

        return context


class DetailOrder(DetailView):
    template_name = 'procurement/detail_order.html'
    model  = OrderInfo
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orderInfo = self.object

        return context



class CreateRequest(CreateView):
    template_name = 'procurement/create_request.html'
    form_class = CreateFormRequest

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
    
            # requestNumの設定
            currentYear= datetime.date.today().year
            currentYearStr = str(currentYear)
            currentYearRequestNums = OrderRequest.objects.values('requestNum').filter(
                submissionDate__year=currentYear)
            lastRequestNum = currentYearRequestNums.aggregate(Max('requestNum'))
            maxRequestNum = lastRequestNum['requestNum__max']

            if (maxRequestNum == None) or (maxRequestNum < 1):
                obj.requestNum = int(currentYearStr[-2:] + "0001")
            else:
                obj.requestNum = maxRequestNum +1

            obj.save()
            return redirect('procurement:detail_request', pk= obj.id)


class CreateOrder(CreateView):
    template_name = 'procurement/create_order.html'
    form_class = CreateFormOrder

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            # orderNumの設定
            currentYear= datetime.date.today().year
            currentYearStr = str(currentYear)
            currentYearOrderNums = OrderInfo.objects.values('orderNum').filter(
                orderDate__year=currentYear
                )
            lastOrderNum = currentYearOrderNums.aggregate(Max('orderNum'))
            maxOrderNum = lastOrderNum['orderNum__max']

            if (maxOrderNum == None) or (maxOrderNum < 1):
                obj.orderNum = int(currentYearStr[-2:] + "0001")
            else:
                obj.orderNum = maxOrderNum +1 
        
            obj.save()
            return redirect('procurement:detail_order', pk= obj.id)


class UpdateRequest(UpdateView):
    template_name = 'procurement/update_request.html'
    model  = OrderRequest
    form_class = UpdateFormRequest

    def get_success_url(self):
        return reverse('procurement:detail_request', kwargs={'pk': self.object.id})


class UpdateOrder(UpdateView):
    template_name = 'procurement/update_order.html'
    model  = OrderInfo
    form_class = UpdateFormOrder

    def get_success_url(self):
        return reverse('procurement:detail_order', kwargs={'pk': self.object.id})

