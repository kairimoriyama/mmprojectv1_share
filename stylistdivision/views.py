from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q, Max, Sum
from django.core import validators
import unicodecsv as csv
from django.contrib import messages

import datetime
from django.utils import timezone

from staffdb.models import StaffDB, Division
from bankaccount.models import Statement
from .models import ARCheck, ProjectProgress, ProjectCategory, ClientCategory, Client, Settlement, Project
from .forms import  SettlementFilterForm, ProjectFilterForm, CreateProjectForm, UpdateProjectForm

# Create your views here.


class ListProject(ListView):
    template_name = 'stylistdivision/list_project.html'
    model  = Project
    fields = '__all__'
    paginate_by = 21
    queryset = Project.objects.all().order_by('projectNum')


    def __init__(self, **kwargs):
        super(ListProject, self).__init__(**kwargs)
        self.form = None


    def get_context_data(self, **kwargs):
        context = super(ListProject, self).get_context_data(**kwargs)

        # 検索結果を保持
        context.update(dict(form=self.form, query_string=self.request.GET.urlencode()))
        
        # 検索フォーム
        context['search_form'] = ProjectFilterForm()

        # 件数表示
        context['items_count'] = self.get_queryset().count()
    
        # 金額表示
        context['items_amount_sales'] = self.get_queryset().aggregate(salesTotal=Sum("salesTotal_exctax"))
        context['items_amount_cost'] = self.get_queryset().aggregate(costTotal=Sum("costTotal_exctax"))

        return context


    def get_queryset(self):
        queryset = super().get_queryset()
       
        projectProgress = self.request.GET.get('projectProgress')
        client = self.request.GET.get('client')
        projectCategory = self.request.GET.get('projectCategory')
        projectName = self.request.GET.get('projectName')
        description = self.request.GET.get('description')

        projectDateFrom = self.request.GET.get('projectDateFrom')
        projectDateTo = self.request.GET.get('projectDateTo')

        invoiceDateFrom = self.request.GET.get('invoiceDateFrom')
        invoiceDateTo = self.request.GET.get('invoiceDateTo')

        salesAmountFrom = self.request.GET.get('salesAmountFrom')
        salesAmountTo = self.request.GET.get('salesAmountTo')

        self.request.session['projectProgress'] = projectProgress
        self.request.session['client'] = client
        self.request.session['projectCategory'] = projectCategory
        self.request.session['projectName'] = projectName
        self.request.session['description'] = description

        self.request.session['projectDateFrom'] = projectDateFrom
        self.request.session['projectDateTo'] = projectDateTo

        self.request.session['invoiceDateFrom'] = invoiceDateFrom
        self.request.session['invoiceDateTo'] = invoiceDateTo
        
        self.request.session['salesAmountFrom'] = salesAmountFrom
        self.request.session['salesAmountTo'] = salesAmountTo

        # 絞り込み前の初期値
        queryset0 = Project.objects.all().order_by('projectPeriodFrom')

        # ページ遷移直後でなければ値がNullではないため絞込可能
        if projectProgress or client or projectCategory or\
            projectName or description or \
            projectDateFrom or projectDateTo or\
            invoiceDateFrom or invoiceDateTo or\
            salesAmountFrom or salesAmountTo  :

            if projectProgress:
                queryset1 = queryset0.filter(projectProgress__id=projectProgress)
            else:
                queryset1 = queryset0.all()

            if client:
                queryset2 = queryset1.filter(client__id=client)
            else:
                queryset2 = queryset1.all()

            if projectCategory:
                queryset3 = queryset2.filter(projectcategory__id=projectCategory)
            else:
                queryset3 = queryset2.all()

            if projectName:
                queryset4 = queryset3.filter(projectName__contains=projectName)
            else:
                queryset4 = queryset3.all()

            if description:
                queryset5 = queryset4.filter(description__contains=description)
            else:
                queryset5 = queryset4.all()

            # 日付の絞込
            if projectDateFrom and projectDateTo :
                queryset6 = queryset5.filter(
                     (Q(projectPeriodFrom__gte=projectDateFrom), Q(projectPeriodFrom__lte=projectDateTo))|
                     (Q(projectDateTo_gte=projectDateFrom), Q(projectDateTo__lte=projectDateTo))
                     )

            elif projectDateFrom and not projectDateTo :
                queryset6 = queryset5.filter(
                    projectPeriodFrom__gte=projectDateFrom)

            elif not projectDateFrom and projectDateTo :
                queryset6 = queryset5.filter(
                     Q(projectPeriodFrom__lte=projectDateTo),
                     Q(projectPeriodTo__lte=projectDateTo)
                    )

            else:                 
                queryset6 = queryset5.all()


            # if invoiceDateFrom and invoiceDateTo :
            #     queryset6 = queryset5.filter(
            #          Q(projectPeriodFrom__gte=projectDateFrom),
            #          Q(projectPeriodTo__lte=projectDateTo)
            #          )

            # elif projectDateFrom and not projectDateTo :
            #     queryset6 = queryset5.filter(
            #         projectPeriodFrom__gte=projectDateFrom)

            # elif not projectDateFrom and projectDateTo :
            #     queryset6 = queryset5.filter(
            #         projectPeriodFrom__lte=projectDateTo)

            # else:                 
            #     queryset6 = queryset5.all()



            # 金額の絞り込み（自・至）
            if salesAmountFrom and salesAmountTo:
                queryset7 = queryset6.filter(salesTotal_exctax__range=(salesAmountFrom, salesAmountTo))

            # 金額の絞り込み（自）
            elif salesAmountFrom and (not salesAmountTo):
                queryset7 = queryset6.filter(salesTotal_exctax__gte=salesAmountFrom)

            # 金額の絞り込み（至）
            elif (not salesAmountFrom) and salesAmountTo:
                queryset7 = queryset6.filter(salesTotal_exctax__lte=salesAmountTo)

            elif (not salesAmountFrom) and (not salesAmountTo):
                queryset7 = queryset6.all()

            queryset = queryset7

            print(queryset)

        # ページ遷移直後のNullでは絞込なし
        else:
            qeryset = queryset0
        
        return queryset.order_by('projectPeriodFrom')

    def post(self, request):

        if request.method == 'POST':
            print("post")

            if 'export_csv' in request.POST:
                print("export_csv")

                queryset = self.get_queryset()

                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="stylist_project.csv"; unicode="utf_8_sig"'

                writer = csv.writer(response, delimiter=',', encoding='utf_8_sig')

                writer.writerow(['id','No.','進捗','納品日・期間（自）','納品日・期間（至）',
                    '日時詳細','場所','顧客','先方担当','種別','案件名','当社担当',
                    'スタイリスト1','スタイリスト2','スタイリスト3','アシスタント1','アシスタント2','アシスタント3',
                    'メモ','税抜売上','税抜費用'])
                for item in queryset.order_by('-projectNum'):
                    writer.writerow([item.id,item.projectNum,item.projectProgress,item.projectPeriodFrom,item.projectPeriodTo,
                    item.projectPeriodDetail, item.location,item.client,item.clientDetail,item.projectcategory,item.projectName,item.mSatff,
                    item.staff1,item.staff2,item.staff3,item.assistant1,item.assistant2,item.assistant3,
                    item.description,item.salesTotal_exctax,item.costTotal_exctax])
                
                return response
        
        return redirect('stylistdivision:list_project')



class DetailProject(DetailView):
    template_name = 'stylistdivision/detail_project.html'
    model  = Project



class CreateProject(CreateView):
    template_name = 'stylistdivision/create_project.html'
    form_class = CreateProjectForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            obj.createdDate = datetime.date.today()

            # 税抜合計の計算

            salses = (obj.salesAmount1_inctax + obj.salesAmount2_inctax + obj.salesAmount2_inctax)/1.1 \
                + obj.salesAmount2_notax + obj.salesAmount3_notax

            obj.salesTotal_exctax = round(salses)

            cost = (obj.costAmount1_inctax + obj.costAmount2_inctax + obj.costAmount3_inctax)/1.1 \
                + obj.costAmount2_notax + obj.costAmount3_notax
    
            obj.costTotal_exctax = round(cost)
    
            # requestNumの設定
            currentYear= datetime.date.today().year
            currentYearStr = str(currentYear)
            currentYearProjectNums = Project.objects.values('projectNum').filter(
                createdDate__year=currentYear)
            lastProjectNum = currentYearProjectNums.aggregate(Max('projectNum'))
            maxProjectNum = lastProjectNum['projectNum__max']

            if (maxProjectNum == None) or (maxProjectNum < 1):
                obj.projectNum = int(currentYearStr[-2:] + "0001")
            else:
                obj.projectNum = maxProjectNum +1

            obj.save()
            return redirect('stylistdivision:detail_project', pk= obj.id)
        
        else:
            return render(request, self.template_name ) 



class UpdateProject(UpdateView):
    template_name = 'stylistdivision/update_project.html'
    model  = Project
    form_class = UpdateProjectForm
    

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()

        sales = (post.salesAmount1_inctax + post.salesAmount2_inctax + post.salesAmount3_inctax)/1.1 \
            + post.salesAmount2_notax + post.salesAmount3_notax

        post.salesTotal_exctax = round(sales)

        cost = (post.costAmount1_inctax + post.costAmount2_inctax + post.costAmount3_inctax)/1.1 \
            + post.costAmount2_notax + post.costAmount3_notax

        post.costTotal_exctax = round(cost)

        post.save()
        return redirect('stylistdivision:detail_project', pk=post.pk)



class ListClient(ListView):
    template_name = 'stylistdivision/list_client.html'
    model  = Client
    fields = '__all__'
    queryset = Client.objects.all().order_by('kanaName')


class DetailClient(DetailView):
    template_name = 'stylistdivision/detail_client.html'
    model  = Client
    fields = '__all__'

class CreateClient(CreateView):
    template_name = 'stylistdivision/create_client.html'
    model  = Client
    fields = '__all__'

    def get_success_url(self):
        return reverse('stylistdivision:detail_client', kwargs={'pk': self.object.id})


class UpdateClient(UpdateView):
    template_name = 'stylistdivision/update_client.html'
    model  = Client
    fields = '__all__'

    def get_success_url(self):
        return reverse('stylistdivision:detail_client', kwargs={'pk': self.object.id})





class ListSettlement(ListView):
    template_name = 'stylistdivision/list_settlement.html'
    model  = Settlement
    paginate_by = 21
    fields = '__all__'
    queryset = Settlement.objects.all().order_by('no')

    def __init__(self, **kwargs):
        super(ListSettlement, self).__init__(**kwargs)
        self.form = None

    def get_context_data(self, **kwargs):
        context = super(ListSettlement, self).get_context_data(**kwargs)

        # 検索結果を保持
        context.update(dict(form=self.form, query_string=self.request.GET.urlencode()))

        # 検索フォーム
        context['search_form'] = SettlementFilterForm()

        # 件数表示
        context['item_count'] = self.get_queryset().count()

        return context


    def get_queryset(self):
        queryset = super().get_queryset()

        arCheck = self.request.GET.get('arCheck')
        description2 = self.request.GET.get('description2')
        memo = self.request.GET.get('memo')
        transactionDateFrom = self.request.GET.get('transactionDateFrom')
        transactionDateTo = self.request.GET.get('transactionDateTo')
        amountFrom = self.request.GET.get('amountFrom')
        amountTo = self.request.GET.get('amountTo')

        self.request.session['arCheck'] = arCheck
        self.request.session['description2'] = description2
        self.request.session['memo'] = memo
        self.request.session['transactionDateFrom'] = transactionDateFrom
        self.request.session['transactionDateTo'] = transactionDateTo
        self.request.session['amountFrom'] = amountFrom
        self.request.session['amountTo'] = amountTo

        # 絞り込み前の初期値
        queryset0 = Settlement.objects.all().order_by('no')

        # ページ遷移直後でなければ値がNullではないため絞込可能
        if arCheck or description2 or memo or\
            transactionDateFrom or transactionDateTo or \
            amountFrom or amountTo:

            if arCheck:
                queryset1 = queryset0.filter(arCheck__id=arCheck)
            else:
                queryset1 = queryset0.all()

            if description2:
                queryset2 = queryset1.filter(statement__description2__icontains=description2)
            else:
                queryset2 = queryset1.all()

            if memo:
                queryset3 = queryset2.filter(
                    Q(memo__icontains=memo) | Q(statement__adminMemo__icontains=memo)
                    )
            else: 
                queryset3 = queryset2.all()

            # 日付の絞込（自）
            if transactionDateFrom :
                queryset4 = queryset3.filter(
                    statement__transactionDate__gte=transactionDateFrom)
            else:                 
                queryset4 = queryset3.all()


            # 日付の絞込（至）
            if transactionDateTo :
                queryset5 = queryset4.filter(
                    statement__transactionDate__lte=transactionDateTo)
            else:                 
                queryset5 = queryset4.all()


            # 金額の絞り込み（自・至）
            if amountFrom and amountTo:
                queryset6 = queryset5.filter(statement__deopsitAmount__range=(amountFrom, amountTo))

            # 金額の絞り込み（自）
            elif amountFrom and (not amountTo):
                queryset6 = queryset5.filter(statement__deopsitAmount__gte=amountFrom)

            # 金額の絞り込み（至）
            elif (not amountFrom) and amountTo:
                queryset6 = queryset5.filter(statement__deopsitAmount__lte=amountTo)

            elif (not amountFrom) and (not amountTo):
                queryset6 = queryset5.all()

            queryset = queryset6

        # ページ遷移直後のNullでは絞込なし
        else:
            qeryset = queryset0
        
        return queryset.order_by('no')


    def post(self, request, *args, **kwargs):

        if request.method == 'POST':

            # データ取込ボタン
            if ('bt_updateStatement' in request.POST):
                print('bt_updateStatement')

                #1102はスタイリスト事業部振込
                q_false = Statement.objects.all().filter(journalCategory__no=1102,divisionCheck=False).order_by('-id')
                q_count_false = q_false.count()

                if q_count_false == 0:
                    print("チェック済み")
                    return self.get(request, *args, **kwargs)

                else:
            
                    for i in range(q_count_false):

                        # 参照対象を定義 #1102はスタイリスト事業部振込
                        record = Statement.objects.all().filter(
                            journalCategory__no=1102,divisionCheck=False).order_by('id').first() 

                        # 年月日コード transactionDate
                        record_transactionDate = record.transactionDate
                        transactionY_code = record_transactionDate.strftime('%Y')[-2:]
                        transactionM_code = record_transactionDate.strftime('%m').zfill(2)
                        transactionD_code = record_transactionDate.strftime('%d').zfill(2)

                        transactionDate_code = transactionY_code + transactionM_code + transactionD_code

                        # 同一年月日のレコード数 #1102はスタイリスト事業部振込
                        recordCount = Statement.objects.all().filter(
                            journalCategory__no=1102,divisionCheck=True,transactionDate=record_transactionDate).count()
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

