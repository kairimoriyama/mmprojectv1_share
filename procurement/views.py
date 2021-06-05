from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q, Max
from django.forms import model_to_dict
from django.core import validators
import unicodecsv as csv
from django.contrib import messages


import datetime
from django.utils import timezone

from .models import AdminCheck, Division, DeliveryAddress, ItemCategory, OrderRequest, OrderInfo, Purpose, PaymentMethod, Progress, Supplier, StandardItem
from .forms import  CreateFormRequest, CreateFormOrder, UpdateFormRequest ,UpdateFormOrder

# Create your views here.


class ListALL(ListView):
    template_name = 'procurement/list_all.html'
    model  = OrderRequest
    fields = '__all__'
    queryset = OrderRequest.objects.filter(deletedItem=False
    ).order_by('adminCheck__no').exclude(adminCheck__gte=5)

    def get_context_data(self, **kwargs):
        context = super(ListALL, self).get_context_data(**kwargs)
        context.update({
            'object_list_order': OrderInfo.objects.order_by('progress__no').exclude(progress__gte=3),
        })

        context['divisionSelect_list'] = Division.objects.all()

        return context
    
    # 検収・発注報告をPOSTメソッドにより実施
    def post(self, request, *args, **kwargs):
       
        # 検収入力フォーム

        if request.method == 'POST':

            # 検収ボタン
            if 'button_acceptance' in request.POST:

                # HTMLから取得したorder
                acceptanceStaff = self.request.POST.get('staff_acceptance')
                acceptanceStaffDivision = self.request.POST.get('division_acceptance')
                acceptanceDate = self.request.POST.get('acceptanceDate_acceptance')
                acceptanceMemo = self.request.POST.get('acceptanceMemo_acceptance')
                selected_order_pk_acceptance = self.request.POST.get('selected_order_pk_acceptance')

                # リスト型
                selected_request_pk_acceptance = []
                # HTMLから取得したrequest カンマ区切りでリスト型へ
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

            # 発注準備ボタン
            if 'button_selectSupplier' in request.POST:

                # HTMLから取得した値
                adminStaff = self.request.POST.get('selectSupplier_adminStaff')

                # リスト型
                selected_request_pk_selectSupplier = []
                # カンマ区切りでリスト型へ
                selected_request_pk_selectSupplier = self.request.POST.get('selected_request_pk_selectSupplier').split(sep=',')


                if adminStaff is None or adminStaff == "":
                    pass

                else:
                    # 依頼を更新
                    for selectSupplier_request_pk in selected_request_pk_selectSupplier:
                        print(selectSupplier_request_pk)
                        orderRequestSelectSupplier = get_object_or_404(OrderRequest, pk=selectSupplier_request_pk)
                        adminCheckSelectSupplier = get_object_or_404(AdminCheck, pk=2)

                        # リストで全件更新
                        orderRequestSelectSupplier.adminStaff = adminStaff
                        orderRequestSelectSupplier.adminCheck = adminCheckSelectSupplier

                        orderRequestSelectSupplier.save()

                print('発注準備')
            

            # 発注報告ボタン
            if 'button_report_order' in request.POST:

                if self.request.POST.get('diff_amount_int') and (int(self.request.POST.get('request_amount_int')) >0 and int(self.request.POST.get('order_amount_int')) >0 and int(self.request.POST.get('diff_amount_int')) == 0) :

                    # 注文の検収情報を更新
                    selected_order_pk_orderReport = self.request.POST.get('selected_order_pk_orderReport')
                    print("報告対象 発注番号" + selected_order_pk_orderReport)
                
                    orderInfoOrderReport = get_object_or_404(OrderInfo, pk=selected_order_pk_orderReport)

                    # Foreignkey Progress
                    progressOrderReport = get_object_or_404(Progress, pk=2)
                    orderInfoOrderReport.progress = progressOrderReport
                    orderInfoOrderReport.save()

                    selected_request_pk_orderReport = self.request.POST.get('selected_request_pk_orderReport')
                    print("報告対象 依頼番号" + selected_request_pk_orderReport)

                    # リスト型
                    selected_request_pk_orderReport = []
                    # カンマ区切りでリスト型へ
                    selected_request_pk_orderReport = self.request.POST.get('selected_request_pk_orderReport').split(sep=',')

                    # 依頼を更新
                    for orderReport_request_pk in selected_request_pk_orderReport:
                        print(orderReport_request_pk)
                        orderRequestOrderReport = get_object_or_404(OrderRequest, pk=orderReport_request_pk)
                        adminCheckOrderReport = get_object_or_404(AdminCheck, pk=4)

                        # リストで全件更新
                        orderRequestOrderReport.adminCheck = adminCheckOrderReport
                        orderRequestOrderReport.orderInfo = orderInfoOrderReport

                        orderRequestOrderReport.save()

                    print('発注報告')
                    return self.get(request, *args, **kwargs)
                else:
                    return self.get(request, *args, **kwargs)
            else:
                return self.get(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)
        



class ListRequest(ListView):
    template_name = 'procurement/list_request.html'
    model  = OrderRequest
    fields = '__all__'
    queryset = OrderRequest.objects.filter(deletedItem=False
    ).order_by('adminCheck__no')
    paginate_by = 22

class ListOrder(ListView):
    template_name = 'procurement/list_order.html'
    model  = OrderInfo
    fields = '__all__'
    queryset = OrderInfo.objects.filter(deletedItem=False).order_by('-id').order_by('progress__no')
    paginate_by = 22




class DetailRequest(DetailView):
    template_name = 'procurement/detail_request.html'
    model  = OrderRequest
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orderRequest = self.object

        # clone するため
        self.request.session['clone_pk'] = str(self.object.pk)
        print(self.request.session['clone_pk'])

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

        form = self.form_class(request.POST, request.FILES)
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

        form = self.form_class(request.POST, request.FILES)
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


def ajax_get_costCenter1(request):
    pk = request.GET.get('pk')
    print('pk:'+pk)
    # pkなし
    if not pk:
        division_list = Division.objects.all()

    # pkあり 
    else:
        division_list = Division.objects.filter(requestStaffDivision__pk=pk)
        print(category_list)

    division_list = [{'pk': costCenter1.pk,'no': costCenter1.pk,'name': costCenter1.name} for costCenter1 in division_list]

    # JSON
    return JsonResponse({'categoryList': division_list})


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

