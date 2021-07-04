from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .models import Statement, BankAccount, JournalCategory
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
import datetime
import csv
import io
from django.db.models import Max


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

        # 口座情報
        context['bankAccount_list'] = BankAccount.objects.all()
        
        # 会計区分
        context['journalCategory_list'] = JournalCategory.objects.all()

        # 件数表示
        context['item_count'] = self.get_queryset().count()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
            
        # 入力した検索条件の取得
        selected_bankAccount = self.request.POST.get('selected_bankAccount')
        print(selected_bankAccount)

        #  値をセッションで保持        
        self.request.session['selected_bankAccount'] = selected_bankAccount

        # 絞り込み前の初期値
        queryset0 = Statement.objects.all().order_by('-id')

        # ページ遷移直後でなければ値がNullではないため絞込可能
        if selected_bankAccount:
            queryset1 = queryset0.filter(bankAccount__id=selected_bankAccount)
            print(selected_bankAccount)

            queryset = queryset1.order_by('-id')

        # ページ遷移直後のNullでは絞込なし
        else:
            qeryset = queryset0.order_by('-id')
        
        return queryset


    def post(self, request, *args, **kwargs):
    
        if request.method == 'POST':

            # データ取込ボタン
            if 'bt_import' in request.POST:
                print('bt_import')

                if 'csv' in request.FILES:
                    
                    data = io.TextIOWrapper(request.FILES['csv'].file, encoding='shift-jis')
                    print(data)
                    csv_content = csv.reader(data)
                    print(type(csv_content))

                    selected_bankAccount = self.request.POST.get('selected_bankAccount')
                    print(selected_bankAccount)

                    bankAccount_obj = get_object_or_404(BankAccount, pk=selected_bankAccount)
                    
                    for row in csv_content:
                        
                        max_id = Statement.objects.aggregate(Max('id'))
                        new_id = int(max_id["id__max"]) +1

                        item, created = Statement.objects.get_or_create(pk=new_id)

                        item.bankAccount = bankAccount_obj

                        item.dateDescription = row[0]
                        item.description1 = row[1]
                        item.description2 = row[2]
                        item.paymentAmount = row[3]
                        item.deopsitAmount = row[4]
                        item.accountBalance = row[5]

                        item.save()
                    return redirect('bankaccount:list_all')
                else:
                    return redirect('bankaccount:list_all')

            # データ整理ボタン
            if 'bt_correspondence' in request.POST:
                    
                selected_bankAccount = self.request.POST.get('selected_bankAccount')
                print(selected_bankAccount)

                queryset =Statement.objects.all().order_by('id')

                # 指定した口座についてレコードの件数
                q_count = Statement.objects.all().filter(
                    bankAccount__id=selected_bankAccount).count()-1
                print(q_count)

                # 更新の必要がなければ終了
                q_count_true = Statement.objects.all().filter(
                    bankAccount__id=selected_bankAccount,consistencyCheck=True).count()-1
                t = q_count - q_count_true

                if t == 0:
                    print("クリーン済み")
                    pass

                else:

                    # チェック対象を定義
                    q_count_update = Statement.objects.all().filter(
                        bankAccount__id=selected_bankAccount,consistencyCheck=False).count()
                    print(q_count_update)
                    
                    record_first = Statement.objects.all().filter(
                        bankAccount__id=selected_bankAccount,consistencyCheck=False).order_by('id').first()
                    print(record_first.id)

                    for i in range(q_count_update):

                        # チェック対象を定義
                        record = Statement.objects.all().get(id=int(record_first.id + i))

                        # 比較対象を定義
                        compare_record = Statement.objects.all().filter(id__lt=int(record_first.id + i)).order_by('id').last()
                        accountBalance1 = compare_record.accountBalance

                        if record.consistencyCheck == True:
                            pass

                        else:
                            # 日付の更新
                            dateDescription1 = record.dateDescription
                            dateDescription2 = datetime.datetime.strptime(dateDescription1, '%Y.%m.%d')
                            record.transactionDate = dateDescription2

                            # 金額整合性
                            paymentAmount = record.paymentAmount
                            deopsitAmount = record.deopsitAmount
                            accountBalance2 = record.accountBalance

                            amount_check = accountBalance1 - paymentAmount + deopsitAmount -accountBalance2
                            if amount_check == 0:
                                record.consistencyCheck = True
                                record.save() # 保存

                            else :
                                record.consistencyCheck = False
                                record.delete() # 削除

                    # 更新後データ
                    q_count_clean = Statement.objects.all().filter(
                        bankAccount__id=selected_bankAccount).count()-1 

                    for j in range(q_count_clean):

                        # 更新対象を定義
                        record_clean = Statement.objects.all().filter(
                            bankAccount__id=selected_bankAccount).order_by('id')[j+1]
                        
                        if record_clean.no:
                            pass
                        else:
                            # 番号を更新
                            record_clean.no = int(Statement.objects.all().filter(
                                bankAccount__id=selected_bankAccount).order_by('id')[j].no) + 1
                            record_clean.save() # 保存

                return redirect('bankaccount:list_all')

            else:
                return self.get(request, *args, **kwargs)

        else:
            return self.get(request, *args, **kwargs)


class DetailStatement(DetailView):
    template_name = 'bankaccount/detail_statement.html'
    model  = Statement
