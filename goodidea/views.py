from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.core import validators
import unicodecsv as csv


import datetime 

from .models import Item, Progress, Division, Category
from .forms import  ProgressSelectForm, DivisionSelectForm,ItemCreateFromIdea, ItemCreateFromAction, ItemUpdateFrom

# Create your views here.

    
class ItemListALL(ListView):
    template_name = 'goodidea/list_all.html'
    model  = Item
    fields = '__all__'
    queryset =Item.objects_list.all_list().order_by('-itemNum')
    paginate_by = 22


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_type'] = 'list_all'
        return context


def item_export(request):
    template_name = 'goodidea/export.html'
    success_url = reverse_lazy('goodidea:list_all')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="goodidea.csv"; unicode="shift-jis"'

    writer = csv.writer(response, delimiter=',', encoding='shift-jis')

    writer.writerow(['番号','協議案件No','共有案件No',
        '登録日','進捗','提案者','所属',
        '分類','購入','システム','提案・実施内容','根拠',
        'URL1','URL2','URL3',
        '写真1','写真2','写真3','写真4','写真5','写真6',
        '資料1','資料2','資料3',
        '検討日','議事録','実施担当者','実施部門','方針・報告','完了日','期日','管理用','削除'])
    for item in Item.objects.all():
        writer.writerow([item.itemNum,item.ideaNum,item.actionNum,
        item.submissionDate,item.progress,item.staff,item.division,
        item.category,item.purchase,item.system,item.title,item.description,
        item.refURL1,item.refURL2,item.refURL3,
        item.picture1,item.picture2,item.picture3,item.picture4,item.picture5,item.picture6,
        item.refFile1,item.refFile2,item.refFile3,
        item.discussionDate,item.discussionNote,item.report,item.inchargeDivision,
        item.inchargeStaff,item.completionDate,item.dueDate,item.adminMemo,item.deletedItem])

    return response


class ItemListDue(ListView):
    template_name = 'goodidea/list_due.html'
    fields = '__all__'
    paginate_by = 22
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_type'] = 'list_due'
        return context

    def get_queryset(request):
        return Item.objects_list.due_list().order_by('-itemNum').order_by('dueDate')




class ItemListFilter(ListView):
    template_name = 'goodidea/list_filter.html'
    model  = Item
    form_class = ProgressSelectForm, DivisionSelectForm
    paginate_by = 22

    def __init__(self, **kwargs):
        super(ItemListFilter, self).__init__(**kwargs)
        self.form = None
    
    def get_context_data(self, **kwargs):
        context = super(ItemListFilter, self).get_context_data(**kwargs)

        # 検索結果を保持
        context.update(dict(form=self.form, query_string=self.request.GET.urlencode()))

        context['progressSelect_list'] = Progress.objects.all()
        context['divisionSelect_list'] = Division.objects.all()

        context['list_type'] = 'list_filter'


        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        
     
        # 入力した検索条件の取得
        progress = self.request.GET.get('progress')

        purchase = self.request.GET.get('purchase')
        system = self.request.GET.get('system')

        staff = self.request.GET.get('staff')
        division = self.request.GET.get('division')
        inchargeStaff = self.request.GET.get('inchargeStaff')
        inchargeDivision = self.request.GET.get('inchargeDivision')
        word = self.request.GET.get('word')
        submissionDateFrom = self.request.GET.get('submissionDateFrom')
        submissionDateTo = self.request.GET.get('submissionDateTo')
        completionDateFrom = self.request.GET.get('completionDateFrom')
        completionDateTo = self.request.GET.get('completionDateTo')
        ideaOrAction = self.request.GET.get('ideaOrAction')


        #  値をセッションで保持
        self.request.session['progress'] = progress
        
        self.request.session['purchase'] = purchase
        self.request.session['system'] = system
        
        self.request.session['staff'] = staff
        self.request.session['division'] = division
        self.request.session['inchargeStaff'] = inchargeStaff
        self.request.session['inchargeDivision'] = inchargeDivision
        self.request.session['word'] = word
        self.request.session['submissionDateFrom'] = submissionDateFrom
        self.request.session['submissionDateTo'] = submissionDateTo
        self.request.session['completionDateFrom'] = completionDateFrom
        self.request.session['completionDateTo'] = completionDateTo
        self.request.session['ideaOrAction'] = ideaOrAction

        # 絞り込み前の初期値
        queryset0 = Item.objects_list.all_list().order_by('-itemNum')

        # ページ遷移直後でなければ値がNullではないため絞込可能
        if progress or purchase or system or staff or division or inchargeStaff or inchargeDivision or word or\
            (submissionDateFrom and submissionDateTo) or (completionDateFrom and completionDateTo):

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
            if staff:
                queryset7 = queryset6.filter(staff__icontains=staff)
            else: 
                queryset7 = queryset6.all()
            
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

            # セッションで選択されたデータを保持
            self.request.session['item_list_type'] = 'filter'
            
            queryset = queryset10.order_by('-itemNum')

        # ページ遷移直後のNullでは絞込なし
        else:
            qeryset = queryset0.order_by('-itemNum')
        
        return queryset.order_by('-itemNum')


class ItemDetail(DetailView):
    template_name = 'goodidea/detail_item.html'
    model  = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        item_list_queryset = Item.objects_list.all_list()

        prev = item_list_queryset
        next = item_list_queryset

        context['prev'] = prev
        context['next'] = next
        return context



class ItemDetailFilter(DetailView):
    template_name = 'goodidea/detail_filter.html'
    model  = Item

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        # 検索条件のパターン
        item_list_type = self.request.session.get('item_list_type')

        # 検索条件を呼び出して必要なitemのみ表示
        progress = self.request.session['progress']
        purchase = self.request.session['purchase']
        system = self.request.session['system']
        staff = self.request.session['staff']
        division = self.request.session['division']
        inchargeStaff = self.request.session['inchargeStaff']
        inchargeDivision = self.request.session['inchargeDivision']
        word = self.request.session['word']
        submissionDateFrom = self.request.session['submissionDateFrom']
        submissionDateTo = self.request.session['submissionDateTo']

        completionDateFrom = self.request.session['completionDateFrom']
        completionDateTo = self.request.session['completionDateTo']
        ideaOrAction = self.request.session['ideaOrAction']
  
        # 絞込み前の初期値
        queryset0 = Item.objects_list.all_list()
        item_list_queryset = queryset0

        if item_list_type == 'filter':

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
            if staff:
                queryset7 = queryset6.filter(staff__icontains=staff)
            else: 
                queryset7 = queryset6.all()
            
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

            item_list_queryset = queryset10
          
        else:
            item_list_queryset = queryset0


        context['prev'] = item_list_queryset.filter(itemNum__gt=item.itemNum).order_by('itemNum').first()
        context['next'] = item_list_queryset.filter(itemNum__lt=item.itemNum).order_by('itemNum').last()

        return context


class ItemDetailDue(DetailView):
    template_name = 'goodidea/detail_due.html'
    model  = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        item_list_queryset = Item.objects_list.all_list()
               
        prev = item_list_queryset
        next = item_list_queryset

        context['prev'] = prev
        context['next'] = next
        return context


class ItemCreateIdea(CreateView):
    template_name = 'goodidea/create_idea.html'
    form_class = ItemCreateFromIdea

    def get_success_url(self):
        return reverse('goodidea:detail_item', kwargs={'pk': self.object.id})



class ItemCreateAction(CreateView):
    template_name = 'goodidea/create_action.html'
    form_class = ItemCreateFromAction
    
    def get_success_url(self):
        return reverse('goodidea:detail_item', kwargs={'pk': self.object.id})



class ItemUpdate(UpdateView):
    template_name = 'goodidea/update_item.html'
    model  = Item
    form_class = ItemUpdateFrom
    
    def get_success_url(self):
        return reverse('goodidea:detail_item', kwargs={'pk': self.object.id})


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
        return reverse('goodidea:detail_due', kwargs={'pk': self.object.id})

