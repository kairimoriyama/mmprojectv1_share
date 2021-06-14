from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.core import validators
import unicodecsv as csv
from staffdb.models import StaffDB

from django.db.models import Max
import datetime
from django.utils import timezone 

from .models import Item, Progress, Division, Category
from .forms import  ProgressSelectForm, DivisionSelectForm,ItemCreateFromIdea, ItemCreateFromAction, ItemUpdateFrom
from staffdb.models import StaffDB

# Create your views here.



class ItemListDue(ListView):
    template_name = 'goodidea/list_due.html'
    fields = '__all__'
    paginate_by = 22

    queryset =Item.objects_list.due_list()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 移動先ページの場合分け
        context['list_type'] = 'list_due'
        return context



class ItemListFilter(ListView):
    template_name = 'goodidea/list_filter.html'
    model  = Item
    form_class = ProgressSelectForm, DivisionSelectForm
    paginate_by = 22

    queryset =Item.objects_list.all_list()

    def __init__(self, **kwargs):
        super(ItemListFilter, self).__init__(**kwargs)
        self.form = None
    
    def get_context_data(self, **kwargs):
        context = super(ItemListFilter, self).get_context_data(**kwargs)

        # 検索結果を保持
        context.update(dict(form=self.form, query_string=self.request.GET.urlencode()))

        context['progressSelect_list'] = Progress.objects.all()
        context['divisionSelect_list'] = Division.objects.all()
        
        # StaffQuerySet のstaff_activeで絞込
        context['staffdb_list'] = StaffDB.objects.staff_active()

        # 移動先ページの場合分け
        context['list_type'] = 'list_filter'


        return context

    def get_queryset(self):
        queryset = super().get_queryset()
       
     
        # 入力した検索条件の取得
        progress = self.request.GET.get('progress')

        purchase = self.request.GET.get('purchase')
        system = self.request.GET.get('system')

        staffdb = self.request.GET.get('staffdb')
        division = self.request.GET.get('division')
        inchargeStaff = self.request.GET.get('inchargeStaff')
        inchargeDivision = self.request.GET.get('inchargeDivision')
        word = self.request.GET.get('word')
        submissionDateFrom = self.request.GET.get('submissionDateFrom')
        submissionDateTo = self.request.GET.get('submissionDateTo')
        completionDateFrom = self.request.GET.get('completionDateFrom')
        completionDateTo = self.request.GET.get('completionDateTo')
        ideaOrAction = self.request.GET.get('ideaOrAction')
        internalDiscussion = self.request.GET.get('internalDiscussion')


        #  値をセッションで保持
        self.request.session['progress'] = progress
        
        self.request.session['purchase'] = purchase
        self.request.session['system'] = system
        
        self.request.session['staffdb'] = staffdb
        self.request.session['division'] = division
        self.request.session['inchargeStaff'] = inchargeStaff
        self.request.session['inchargeDivision'] = inchargeDivision
        self.request.session['word'] = word
        self.request.session['submissionDateFrom'] = submissionDateFrom
        self.request.session['submissionDateTo'] = submissionDateTo
        self.request.session['completionDateFrom'] = completionDateFrom
        self.request.session['completionDateTo'] = completionDateTo
        self.request.session['ideaOrAction'] = ideaOrAction
        self.request.session['internalDiscussion'] = internalDiscussion

        # 絞り込み前の初期値
        queryset0 = Item.objects_list.all_list().order_by('-itemNum')

        # ページ遷移直後でなければ値がNullではないため絞込可能
        if progress or purchase or system or staffdb or division or inchargeStaff or inchargeDivision or word or\
            (submissionDateFrom and submissionDateTo) or (completionDateFrom and completionDateTo) or internalDiscussion:

            # 協議案件/共有案件
            if ideaOrAction == "0":   #協議案件のみ
                queryset1 = queryset0.filter( ideaNum__gt = 0)
            elif ideaOrAction == "1": #共有案件のみ
                queryset1 = queryset0.filter( actionNum__gt = 0)
            else:
                queryset1 = queryset0.all()

            # 購入案件の絞込
            if purchase == "1":
                queryset2 = queryset1.filter(purchase__exact=True)
            else:
                queryset2 = queryset1.all()

            # システム案件の絞込
            if system == "1":
                queryset3 = queryset2.filter(system__exact=True)
            else:
                queryset3 = queryset2.all()

            # 所属の絞り込み
            if division == "0": #全部門
                queryset4 = queryset3.all()
            else:               #全部門以外
                queryset4 = queryset3.filter(division__exact=division)
            
            # 進捗・完了日の絞り込み
            if progress == "0":   #全進捗
                queryset5 = queryset4.all()
            elif progress == "4": #完了案件のみ
                queryset5 = queryset4.filter(progress__exact=4
                ).filter(completionDate__range=(completionDateFrom, completionDateTo))
            else:                 #新規/実施なし
                queryset5 = queryset4.filter(progress__exact=progress)

            # 日付の絞込
            if (submissionDateFrom and submissionDateTo) :
                queryset6 = queryset5.filter(
                    submissionDate__range=(submissionDateFrom, submissionDateTo)
                )
            else:                 
                queryset6 = queryset5.all()

            # 担当者の絞込
            if staffdb == "0":   #全社員
                queryset7 = queryset6.all()
            else: 
                queryset7 = queryset6.filter(staffdb__exact=staffdb)
            
            # 実行担当者の絞込
            if inchargeStaff:
                queryset8 = queryset7.filter(inchargeStaff__icontains=inchargeStaff)
            else: 
                queryset8 = queryset7.all()    

            # 実行担当部署の絞込
            if inchargeDivision:
                queryset9 = queryset8.filter(inchargeDivision__icontains=inchargeDivision)
            else: 
                queryset9 = queryset8.all()   

             # キーワードの絞込
            if word :
                queryset10 = queryset9.filter(
                    Q(title__icontains=word)| Q(description__icontains=word)|
                    Q(discussionNote__icontains=word)| Q(report__icontains=word))
            else: 
                queryset10 = queryset9.all() 


            # 部門決裁の絞り込み
            if internalDiscussion == "1":
                queryset11 = queryset10.filter(internalDiscussion__exact=True)
            else:
                queryset11 = queryset10.all()

            # セッションにて状態を保存
            self.request.session['item_list_type'] = 'filter'
            
            queryset = queryset11.order_by('-itemNum')

        # ページ遷移直後のNullでは絞込なし
        else:
            qeryset = queryset0.order_by('-itemNum')
        
        return queryset.order_by('-itemNum')




class ItemDetailFilter(DetailView):
    template_name = 'goodidea/detail_filter.html'
    model  = Item

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        # 検索条件のパターン
        item_list_type = self.request.session.get('item_list_type')

        print(item_list_type)

        # 検索条件を呼び出して必要なitemのみ表示
        progress = self.request.session['progress']
        purchase = self.request.session['purchase']
        system = self.request.session['system']
        staffdb = self.request.session['staffdb']
        division = self.request.session['division']
        inchargeStaff = self.request.session['inchargeStaff']
        inchargeDivision = self.request.session['inchargeDivision']
        word = self.request.session['word']
        submissionDateFrom = self.request.session['submissionDateFrom']
        submissionDateTo = self.request.session['submissionDateTo']

        completionDateFrom = self.request.session['completionDateFrom']
        completionDateTo = self.request.session['completionDateTo']
        ideaOrAction = self.request.session['ideaOrAction']
        internalDiscussion = self.request.session['internalDiscussion']
  
        # 絞込み前の初期値
        queryset0 = Item.objects_list.all_list()
        item_list_queryset = queryset0


        if item_list_type == 'filter':
                
            if progress or purchase or system or staffdb or division or inchargeStaff or inchargeDivision or word or\
                (submissionDateFrom and submissionDateTo) or (completionDateFrom and completionDateTo) or internalDiscussion:

                # 協議案件/共有案件
                if ideaOrAction == "0":   #協議案件のみ
                    queryset1 = queryset0.filter( ideaNum__gt = 0)
                elif ideaOrAction == "1": #共有案件のみ
                    queryset1 = queryset0.filter( actionNum__gt = 0)
                else:
                    queryset1 = queryset0.all()

                # 購入案件の絞込
                if purchase == "1":
                    queryset2 = queryset1.filter(purchase__exact=True)
                else:
                    queryset2 = queryset1.all()

                # システム案件の絞込
                if system == "1":
                    queryset3 = queryset2.filter(system__exact=True)
                else:
                    queryset3 = queryset2.all()

                # 所属の絞り込み
                if division == "0": #全部門
                    queryset4 = queryset3.all()
                else:               #全部門以外
                    queryset4 = queryset3.filter( division__exact=division)
                
                # 進捗・完了日の絞り込み
                if progress == "0":   #全進捗
                    queryset5 = queryset4.all()
                elif progress == "4": #完了案件のみ
                    queryset5 = queryset4.filter(progress__exact=4
                    ).filter(completionDate__range=(completionDateFrom, completionDateTo))
                else:                 #新規/実施なし
                    queryset5 = queryset4.filter(progress__exact=progress)


                # 日付の絞込
                if (submissionDateFrom and submissionDateTo) :
                    queryset6 = queryset5.filter(
                        submissionDate__range=(submissionDateFrom, submissionDateTo)
                    )
                else:                 
                    queryset6 = queryset5.all()

                # 担当者の絞込
                if staffdb == "0":   #全社員
                    queryset7 = queryset6.all()
                else: 
                    queryset7 = queryset6.filter(staffdb__exact=staffdb)
                
                # 実行担当者の絞込
                if inchargeStaff:
                    queryset8 = queryset7.filter(inchargeStaff__icontains=inchargeStaff)
                else: 
                    queryset8 = queryset7.all()    

                # 実行担当部署の絞込
                if inchargeDivision:
                    queryset9 = queryset8.filter(inchargeDivision__icontains=inchargeDivision)
                else: 
                    queryset9 = queryset8.all()   

                # キーワードの絞込
                if word :
                    queryset10 = queryset9.filter(
                        Q(title__icontains=word)| Q(description__icontains=word)|
                        Q(discussionNote__icontains=word)| Q(report__icontains=word))
                else: 
                    queryset10 = queryset9.all() 
                
                # 部門決裁の絞り込み
                if internalDiscussion == "1":
                    queryset11 = queryset10.filter(internalDiscussion__exact=True)
                else:
                    queryset11 = queryset10.all()

                item_list_queryset = queryset11
            
            else:
                item_list_queryset = queryset0

        else:
            item_list_queryset = queryset0

        context['prev'] = item_list_queryset.filter(itemNum__gt=item.itemNum).order_by('itemNum').first()
        context['next'] = item_list_queryset.filter(itemNum__lt=item.itemNum).order_by('itemNum').last()

        return context


class ItemDetailDue(DetailView):
    template_name = 'goodidea/detail_due.html'
    model  = Item


class ItemCreateIdea(CreateView):
    template_name = 'goodidea/create_idea.html'
    form_class = ItemCreateFromIdea

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            

            # ideaNumの設定
            currentYear= datetime.date.today().year
            currentYearStr = str(currentYear)
            currentYearIdeaNums = Item.objects.values('ideaNum').filter(
                submissionDate__year=currentYear
                )
            lastIdeaNum = currentYearIdeaNums.aggregate(Max('ideaNum'))
            maxIdeaNum = lastIdeaNum['ideaNum__max']

            if (maxIdeaNum == None) or (maxIdeaNum < 1):
                obj.ideaNum = int(currentYearStr[-2:] + "0001")
            else:
                obj.ideaNum = maxIdeaNum +1 

            # itemNumの設定
            ItemNums = Item.objects.values('itemNum')
            lastItemNum = ItemNums.aggregate(Max('itemNum'))
            maxItemNum = lastItemNum['itemNum__max']

            if (maxItemNum == None) or (maxItemNum < 1):
                obj.itemNum = 1
            else:
                obj.itemNum = maxItemNum +1 

            obj.save()
            return redirect('goodidea:detail_filter', pk= obj.id)



class ItemCreateAction(CreateView):
    template_name = 'goodidea/create_action.html'
    form_class = ItemCreateFromAction


    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            
            # actionNumの設定
            currentYear= datetime.date.today().year
            currentYearStr = str(currentYear)
            currentYearActionNums = Item.objects.values('actionNum').filter(
                submissionDate__year=currentYear
                )
            lastActionNum = currentYearActionNums.aggregate(Max('actionNum'))
            maxActionNum = lastActionNum['actionNum__max']

            print(maxActionNum)

            if (maxActionNum == None) or (maxActionNum < 1):
                obj.actionNum = int(currentYearStr[-2:] + "001")
            else:
                obj.actionNum = maxActionNum +1 


            # itemNumの設定
            ItemNums = Item.objects.values('itemNum')
            lastItemNum = ItemNums.aggregate(Max('itemNum'))
            maxItemNum = lastItemNum['itemNum__max']

            if (maxItemNum == None) or (maxItemNum < 1):
                obj.itemNum = 1
            else:
                obj.itemNum = maxItemNum +1 

            obj.save()
            return redirect('goodidea:detail_filter', pk= obj.id )




class ItemUpdateFilter(UpdateView):
    template_name = 'goodidea/update_filter.html'
    model  = Item
    form_class = ItemUpdateFrom
    
    def get_success_url(self):
        return reverse('goodidea:detail_filter', kwargs={'pk': self.object.id})



class ItemUpdateDue(UpdateView):
    template_name = 'goodidea/update_due.html'
    model  = Item
    form_class = ItemUpdateFrom
    
    def get_success_url(self):
        if self.object.progress.no == 2: 
            return reverse('goodidea:detail_due', kwargs={'pk': self.object.id})
        else:
            return reverse('goodidea:detail_filter', kwargs={'pk': self.object.id})



def ajax_get_staff(request):
    staffNumber = request.GET.get('staffNumber')
    # staffNumber入力なし
    if not staffNumber:

        # StaffQuerySet のstaff_active()で絞り込み
        staff_list = StaffDB.objects.staff_active()


    # staffNumber入力あり 
    else:
        # StaffQuerySet のstaff_active()で絞り込み
        staff_list = StaffDB.objects.staff_active().filter(no__startswith=staffNumber)

    staff_list = [{'pk': staff_obj.pk,'no': staff_obj.no,'fullName': staff_obj.fullName} for staff_obj in staff_list]

    # JSON
    return JsonResponse({'staffList': staff_list})



# 先頭に空データ追加の追加あり
def ajax_get_staff_filter(request):
    staffNumber = request.GET.get('staffNumber')
    # staffNumber入力なし
    if not staffNumber:

        # StaffQuerySet のstaff_active()で絞り込み
        staff_list = StaffDB.objects.staff_active()

    # staffNumber入力あり 
    else:
        # StaffQuerySet のstaff_active()で絞り込み
        staff_list = StaffDB.objects.staff_active().filter(no__startswith=staffNumber)

    staff_list = [{'pk': staff_obj.pk,'no': staff_obj.no,'fullName': staff_obj.fullName} for staff_obj in staff_list]

    # 先頭に空データ追加
    dummy_staff = {'pk': 0,'no': 0,'fullName': "-"} 
    staff_list.insert(0, dummy_staff)

    # JSON
    return JsonResponse({'staffList': staff_list})