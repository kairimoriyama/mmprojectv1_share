from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .models import Statement
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
import datetime


# Create your views here.


class StatementList(ListView):
    template_name = 'bankaccount/list_all.html'
    fields = '__all__'
    paginate_by = 21
    queryset =Statement.objects.all().order_by('-no')


def correspondence_amount(request):
    template_name = 'bankaccount/list_all.html'
    success_url = reverse_lazy('bankaccount:list_all')

    queryset =Statement.objects.all().order_by('id')
    q_num = Statement.objects.all().count()-1
    q_num_true = Statement.objects.all().count().filter(consistencyCheck=True)-1

    t = q_num - q_num_true
    if t == 0:
        pass

    else:

        for i in range(q_num):

            # チェック対象を定義
            record = Statement.objects.all().order_by('id')[i+1]

            # 比較対象を定義
            accountBalance1 = Statement.objects.all().order_by('id')[i].accountBalance

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

                    if type(Statement.objects.all().order_by('id')[i].no) == int:
                        record.no = Statement.objects.all().order_by('id')[i].no + 1
                    else:
                        pass

                    record.consistencyCheck = True
                    record.save() # 保存

                else :
                    record.consistencyCheck = False

        error_record = Statement.objects.all().filter(consistencyCheck=False)
        error_record.delete() # 削除

    return render(request,'bankaccount/list_all.html')


