from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .models import Statement, BankAccount, JournalCategory
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import timedelta, date
import csv
import io
from django.db.models import Max
from .forms import  InputForm

# Create your views here.


class StatementList(ListView):
    template_name = 'bankaccount/list_all.html'
    fields = '__all__'
    paginate_by = 21
    queryset =Statement.objects.all().order_by('-id')

    def __init__(self, **kwargs):
        super(StatementList, self).__init__(**kwargs)
        self.form = None

    def get_context_data(self, **kwargs):
        context = super(StatementList, self).get_context_data(**kwargs)

        # 検索結果を保持
        context.update(dict(form=self.form, query_string=self.request.GET.urlencode()))

        # 検索フォーム
        context['search_form'] = InputForm()

        # 件数表示
        context['item_count'] = self.get_queryset().count()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        bankAccount = self.request.GET.get('bankAccount')
        journalCategory = self.request.GET.get('selected_journalCategory')
        arOrAp = self.request.GET.get('arOrAp')
        progress = self.request.GET.get('progress')
        description1 = self.request.GET.get('description1')
        description2 = self.request.GET.get('description2')
        adminMemo = self.request.GET.get('adminMemo')
        transactionDateFrom = self.request.GET.get('transactionDateFrom')
        transactionDateTo = self.request.GET.get('transactionDateTo')
        accountAmountFrom = self.request.GET.get('accountAmountFrom')
        accountAmountTo = self.request.GET.get('accountAmountTo')

        self.request.session['bankAccount'] = bankAccount
        self.request.session['journalCategory'] = journalCategory
        self.request.session['arOrAp'] = arOrAp
        self.request.session['progress'] = progress
        self.request.session['description1'] = description1
        self.request.session['description2'] = description2
        self.request.session['adminMemo'] = adminMemo
        self.request.session['transactionDateFrom'] = transactionDateFrom
        self.request.session['transactionDateTo'] = transactionDateTo
        self.request.session['accountAmountFrom'] = accountAmountFrom
        self.request.session['accountAmountTo'] = accountAmountTo

        # 絞り込み前の初期値
        queryset0 = Statement.objects.all().order_by('-id')

        # ページ遷移直後でなければ値がNullではないため絞込可能
        if bankAccount or journalCategory or arOrAp or description1 or description2 or adminMemo or\
            transactionDateFrom or transactionDateTo or \
            accountAmountFrom or accountAmountTo:

            if bankAccount:
                queryset1 = queryset0.filter(bankAccount__id=bankAccount)
            else:
                queryset1 = queryset0.all()

            if journalCategory:
                queryset2 = queryset1.filter(journalCategory__id=journalCategory)
            else:
                queryset2 = queryset1.all()

            print(arOrAp)

            if arOrAp == "0":
                queryset3_1 = queryset2.filter(deopsitAmount=0)

                # 金額の絞り込み（自・至）
                if accountAmountFrom and accountAmountTo:
                    queryset3_2 = queryset3_1.filter(paymentAmount__range=(accountAmountFrom, accountAmountTo))

                # 金額の絞り込み（自）
                elif accountAmountFrom and (not accountAmountTo):
                    queryset3_2 = queryset3_1.filter(paymentAmount__gte=accountAmountFrom)

                # 金額の絞り込み（自）
                elif (not accountAmountFrom) and accountAmountTo:
                    queryset3_2 = queryset3_1.filter(paymentAmount__lte=accountAmountTo)

                elif (not accountAmountFrom) and (not accountAmountTo):
                    queryset3_2 = queryset3_1.all()

            elif arOrAp == "1":
                queryset3_1 = queryset2.filter(paymentAmount=0)

                # 金額の絞り込み（自・至）
                if accountAmountFrom and accountAmountTo:
                    queryset3_2 = queryset3_1.filter(deopsitAmount__range=(accountAmountFrom, accountAmountTo))

                # 金額の絞り込み（自）
                elif accountAmountFrom and (not accountAmountTo):
                    queryset3_2 = queryset3_1.filter(deopsitAmount__gte=accountAmountFrom)

                # 金額の絞り込み（自）
                elif (not accountAmountFrom) and accountAmountTo:
                    queryset3_2 = queryset3_1.filter(deopsitAmount__lte=accountAmountTo)

                elif (not accountAmountFrom) and (not accountAmountTo):
                    queryset3_2 = queryset3_1.all()

            elif arOrAp == "2":
                queryset3_2 = queryset2.all()

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



    def post(self, request, *args, **kwargs):

        bankAccount = self.request.POST.get('selected_bankAccount', None)
        request.session['bankAccount'] = bankAccount
        print(bankAccount)

        journalCategory = self.request.POST.get('journalCategory', None)
        request.session['journalCategory'] = journalCategory
        print(journalCategory)

        if request.method == 'POST':

            # データ取込ボタン
            if ('bt_import' in request.POST) and bankAccount :
                print('bt_import')

                if 'csv' in request.FILES:
                    
                    data = io.TextIOWrapper(request.FILES['csv'].file, encoding='shift-jis')
                    print(data)
                    csv_content = csv.reader(data)
                    print(type(csv_content))
                   
                    bankAccount_obj = get_object_or_404(BankAccount, pk=bankAccount)
                    journalCategory_obj = get_object_or_404(JournalCategory, id=1) # 仕分け区分「要確認」
                    
                    for row in csv_content:
                        
                        max_id = Statement.objects.aggregate(Max('id'))
                        new_id = int(max_id["id__max"]) +1

                        item, created = Statement.objects.get_or_create(pk=new_id)

                        item.bankAccount = bankAccount_obj
                        item.journalCategory = journalCategory_obj

                        item.dateDescription = row[0]
                        item.description1 = row[1]
                        item.description2 = row[2]
                        item.paymentAmount = row[3]
                        item.deopsitAmount = row[4]
                        item.accountBalance = row[5]

                        item.save()
                        
                    return redirect('bankaccount:list_all')
                else:
                    return self.get(request, *args, **kwargs)
 

            # 仕訳区分の登録
            elif (('bt_journalCategory' in request.POST) and self.request.POST.get('selected_record_list')):
                print('bt_journalCategory')

                # リスト型
                record_list = []
                # HTMLから取得したrecordを カンマ区切りでリスト型へ
                record_list = self.request.POST.get('selected_record_list').split(sep=',')
                print(len(record_list))

                if not journalCategory:
                    print("区分なし")
                    return self.get(request, *args, **kwargs)

                else:
                    
                    # Foreignkey
                    selected_journalCategory = get_object_or_404(JournalCategory, pk=journalCategory)
                    print(selected_journalCategory)

                    # recordを更新
                    for record_id in record_list:
                        record = get_object_or_404(Statement, pk=record_id)

                        if not record.no:
                            print("発番なし")
                            pass
                        else:
                            record.journalCategory = selected_journalCategory 
                            record.save()

                    return self.get(request, *args, **kwargs)      

            # データ整理ボタン
            elif ('bt_correspondence' in request.POST) and bankAccount:

                queryset =Statement.objects.all().order_by('id')

                # 指定した口座についてレコードの件数
                q_count = Statement.objects.all().filter(
                    bankAccount__id=bankAccount).count()-1
                print(q_count)

                # 更新の必要がなければ終了
                q_count_true = Statement.objects.all().filter(
                    bankAccount__id=bankAccount,consistencyCheck=True).count()-1
                t = q_count - q_count_true

                if t == 0:
                    print("クリーン済み")
                    return self.get(request, *args, **kwargs)

                else:

                    # チェック対象を定義
                    q_count_update = Statement.objects.all().filter(
                        bankAccount__id=bankAccount,consistencyCheck=False).count()
                    print(q_count_update)
                    
                    record_first = Statement.objects.all().filter(
                        bankAccount__id=bankAccount,consistencyCheck=False).order_by('id').first()
                    print(record_first.id)

                    for i in range(q_count_update):

                        # チェック対象を定義
                        record = Statement.objects.all().get(id=int(record_first.id + i))

                        # 比較対象を定義
                        compare_record = Statement.objects.all().filter(bankAccount__id=bankAccount,id__lt=int(record_first.id + i)).order_by('id').last()
                        accountBalance1 = compare_record.accountBalance
                        transactionDate1 =compare_record.transactionDate
                        
                        if record.consistencyCheck == True:
                            pass

                        else:
                            # 日付の更新
                            dateDescription1 = record.dateDescription
                            dateDescription2 = datetime.datetime.strptime(dateDescription1, '%Y.%m.%d').date()
                            record.transactionDate = dateDescription2

                            # 金額整合性
                            paymentAmount = record.paymentAmount
                            deopsitAmount = record.deopsitAmount
                            accountBalance2 = record.accountBalance
                            amount_check = accountBalance1 - paymentAmount + deopsitAmount -accountBalance2
                            
                           # 日付整合性
                            transactionDate2 = record.transactionDate

                            if amount_check == 0 and (transactionDate1 <= transactionDate2):

                                # 整合性True
                                record.consistencyCheck = True
                                
                                if record.no:
                                    pass
                                else:
                                        
                                    # 口座情報 id bankAccount
                                    bankAccount_code = str(bankAccount).ljust(2, '0')

                                    # 年月日コード transactionDate
                                    record_transactionDate = record.transactionDate
                                    transactionY_code = record_transactionDate.strftime('%Y')[-2:]
                                    transactionM_code = record_transactionDate.strftime('%m').zfill(2)
                                    transactionD_code = record_transactionDate.strftime('%d').zfill(2)

                                    transactionDate_code = transactionY_code + transactionM_code + transactionD_code

                                    # 同一年月日のレコード数
                                    recordCount = Statement.objects.all().filter(
                                        bankAccount__id=bankAccount,transactionDate=record_transactionDate).count()
                                    recordCount_code = str(recordCount + 1).zfill(3)

                                    # 番号を更新
                                    record.no = int(bankAccount_code + transactionDate_code + recordCount_code)

                                    record.save() # 保存

                            else :
                                record.consistencyCheck = False
                                record.delete() # 削除
                            
                return redirect('bankaccount:list_all')

            else:
                return self.get(request, *args, **kwargs)

        else:
            return self.get(request, *args, **kwargs)


class DetailStatement(DetailView):
    template_name = 'bankaccount/detail_statement.html'
    model  = Statement
