from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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

from staffdb.models import StaffDB, Division
from bankaccount.models import Statement
from .models import ARCheck, ProjectProgress, ProjectCategory, ClientCategory, Client, Settlement, Project
from .forms import  SelectForm

# Create your views here.


class ListProject(ListView):
    template_name = 'stylistdivision/list_project.html'
    model  = Project
    fields = '__all__'
    queryset = Project.objects.all().order_by('no')


class ListSettlement(ListView):
    template_name = 'stylistdivision/list_settlement.html'
    model  = Settlement
    fields = '__all__'
    queryset = Settlement.objects.all().order_by('-id')

    def __init__(self, **kwargs):
        super(ListSettlement, self).__init__(**kwargs)
        self.form = None

    def get_context_data(self, **kwargs):
        context = super(ListSettlement, self).get_context_data(**kwargs)

        # 検索結果を保持
        context.update(dict(form=self.form, query_string=self.request.GET.urlencode()))

        # 検索フォーム
        context['search_form'] = SelectForm()

        # 件数表示
        context['item_count'] = self.get_queryset().count()

        return context

''''
    def get_queryset(self):
        queryset = super().get_queryset()

        arCheck = self.request.GET.get('arCheck')
        description1 = self.request.GET.get('description1')
        memo = self.request.GET.get('memo')
        transactionDateFrom = self.request.GET.get('transactionDateFrom')
        transactionDateTo = self.request.GET.get('transactionDateTo')
        amountFrom = self.request.GET.get('amountFrom')
        amountTo = self.request.GET.get('amountTo')

        self.request.session['arCheck'] = arCheck
        self.request.session['description1'] = description1
        self.request.session['memo'] = memo
        self.request.session['transactionDateFrom'] = transactionDateFrom
        self.request.session['transactionDateTo'] = transactionDateTo
        self.request.session['amountFrom'] = amountFrom
        self.request.session['amountTo'] = amountTo

        # 絞り込み前の初期値
        queryset0 = Settlement.objects.all().order_by('no')

        # ページ遷移直後でなければ値がNullではないため絞込可能
        if arCheck or description1 or memo or\
            transactionDateFrom or transactionDateTo or \
            amountFrom or amountTo:

            if arCheck:
                queryset1 = queryset0.filter(arCheck__id=arCheck)
            else:
                queryset1 = queryset0.all()

            if description1:
                queryset2 = queryset1.filter(statement__description1__icontains=description1)
            else:
                queryset2 = queryset1.all()


            # 金額の絞り込み（自・至）
            if accountAmountFrom and accountAmountTo:
                queryset3_2 = queryset3_1.filter(deopsitAmount__range=(accountAmountFrom, accountAmountTo))

            # 金額の絞り込み（自）
            elif accountAmountFrom and (not accountAmountTo):
                queryset3_2 = queryset3_1.filter(deopsitAmount__gte=accountAmountFrom)

            # 金額の絞り込み（自）
            if (not accountAmountFrom) and accountAmountTo:
                queryset3_2 = queryset3_1.filter(deopsitAmount__lte=accountAmountTo)

            elif (not accountAmountFrom) and (not accountAmountTo):
                queryset3_2 = queryset3_1.all()


            # description1
            if description1:
                queryset4 = queryset3_2.filter(description1__icontains=description1)
            else: 
                queryset4 = queryset3_2.all()

            # description2
            if description2:
                queryset5 = queryset4.filter(description2__icontains=description2)
            else: 
                queryset5 = queryset4.all()    

            # adminMemo
            if adminMemo:
                queryset6 = queryset5.filter(adminMemo__icontains=adminMemo)
            else: 
                queryset6 = queryset5.all()    

            # 日付の絞込（自）
            if transactionDateFrom :
                queryset7 = queryset6.filter(
                    transactionDate__gte=transactionDateFrom)
            else:                 
                queryset7 = queryset6.all()


            # 日付の絞込（至）
            if transactionDateTo :
                queryset8 = queryset7.filter(
                    transactionDate__lte=transactionDateTo)
            else:                 
                queryset8 = queryset7.all()

            queryset = queryset8

        # ページ遷移直後のNullでは絞込なし
        else:
            qeryset = queryset0
        
        return queryset.order_by('-id')
'''

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':

            # データ取込ボタン
            if ('bt_updateStatement' in request.POST):
                print('bt_updateStatement')

                #2001はスタイリスト事業部債権
                q_false = Statement.objects.all().filter(bankAccount__id=3,journalCategory__no=2001,divisionCheck=False).order_by('-id')
                q_count_false = q_false.count()

                if q_count_false == 0:
                    print("チェック済み")
                    return self.get(request, *args, **kwargs)

                else:
            
                    for i in range(q_count_false):

                        # 参照対象を定義 #2001はスタイリスト事業部債権
                        record = Statement.objects.all().filter(
                            bankAccount__id=3,journalCategory__no=2001,divisionCheck=False).order_by('id').first() 

                        # 年月日コード transactionDate
                        record_transactionDate = record.transactionDate
                        transactionY_code = record_transactionDate.strftime('%Y')[-2:]
                        transactionM_code = record_transactionDate.strftime('%m').zfill(2)
                        transactionD_code = record_transactionDate.strftime('%d').zfill(2)

                        transactionDate_code = transactionY_code + transactionM_code + transactionD_code

                        # 同一年月日のレコード数 #2001はスタイリスト事業部債権
                        recordCount = Statement.objects.all().filter(
                            bankAccount__id=3,journalCategory__no=2001,divisionCheck=True,transactionDate=record_transactionDate).count()
                        recordCount_code = str(recordCount + 1).zfill(2)

                        # 番号を更新
                        new_item = Settlement.objects.create(no=int(transactionDate_code + recordCount_code), statement=record )

                        # 番号を更新
                        new_item.transferFee = 0
                        new_item.otherAmount = 0
                        new_item.totalAmount = record.deopsitAmount

                        new_item.save() # 保存

                        # divisionCheck True
                        record.divisionCheck = True  
                        
                        record.save() # 保存

                return redirect('stylistdivision:list_settlement')

            else:
                return self.get(request, *args, **kwargs)
