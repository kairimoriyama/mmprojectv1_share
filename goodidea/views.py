from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db import transaction
<<<<<<< HEAD
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
=======
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
>>>>>>> origin/main
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.core import validators
<<<<<<< HEAD
import unicodecsv as csv

# from django.contrib.auth.mixins import LoginRequiredMixin
=======
import csv
>>>>>>> origin/main

import datetime 

from .models import Item, Progress, Division, Category
from .forms import  ProgressSelectForm, DivisionSelectForm,ItemCreateFromIdea, ItemCreateFromAction, ItemUpdateFrom

# Create your views here.

<<<<<<< HEAD
# class IndexView(TemplateView):
#     template_name = '/home'
    
=======
>>>>>>> origin/main
class ItemListALL(ListView):
    template_name = 'goodidea/list_all.html'
    model  = Item
    fields = '__all__'
    queryset =Item.objects.filter(deletedItem=False).order_by('-id')
    paginate_by = 22

<<<<<<< HEAD

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_type'] = 'list_all'
        return context


def item_export(request):
    template_name = 'goodidea/export.html'
    success_url = reverse_lazy('goodidea:list_all')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="item.csv"'

    response.write("\xEF\xBB\xBF")
    writer = csv.writer(response, delimiter=',', encoding="shift-jis")

    writer.writerow(['案件番号','協議案件番号','完了共有案件番号','登録日','進捗','提案者','所属','分類','提案・実施内容','理由説明','URL1','URL2','URL3','写真1','写真2','写真3','資料1','資料2','資料3','検討日','議事録','担当者','担当部門','方針・報告','完了日','期日','管理用','削除'])
    for item in Item.objects.all():
        writer.writerow([item.itemNum,item.ideaNum,item.actionNum,item.submissionDate,item.progress,item.staff,item.division,item.category,item.title,item.description,item.refURL1,item.refURL2,item.refURL3,item.picture1,item.picture2,item.picture3,item.refFile1,item.refFile2,item.refFile3,item.discussionDate,item.discussionNote,item.report,item.inchargeDivision,item.inchargeStaff,item.completionDate,item.dueDate,item.adminMemo,item.deletedItem])
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
        return Item.objects_list.due_list().order_by('dueDate')


=======
def item_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="item.csv"'
    writer = csv.writer(response)
    writer.writerow(['案件番号','協議案件番号','店舗完了案件番号','登録日','進捗','提案者','所属','分類','提案・実施内容','理由説明','URL1','URL2','URL3','写真1','写真2','写真3','資料1','資料2','資料3','検討日','検討内容','担当者','担当部門','方針・報告','完了日','管理用','削除'])
    for item in Item.objects.all():
        writer.writerow([item.itemNum,item.ideaNum,item.actionNum,item.submissionDate,item.progress,item.staff,item.division,item.category,item.title,item.description,item.refURL1,item.refURL2,item.refURL3,item.picture1,item.picture2,item.picture3,item.refFile1,item.refFile2,item.refFile3,item.discussionDate,item.discussionNote,item.report,item.inchargeDivision,item.inchargeStaff,item.completionDate,item.adminMemo,item.deletedItem])
    return response
    
>>>>>>> origin/main

class ItemListIdea(ListView):
    template_name = 'goodidea/list_idea.html'
    fields = '__all__'
    paginate_by = 22

<<<<<<< HEAD
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_type'] = 'list_idea'
        return context

=======
>>>>>>> origin/main
    def get_queryset(request):
        return Item.objects_list.idea_list().order_by('-itemNum')


class ItemListAction(ListView):
    template_name = 'goodidea/list_action.html'
    fields = '__all__'
    paginate_by = 22
<<<<<<< HEAD
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_type'] = 'list_action'
        return context
=======
>>>>>>> origin/main

    def get_queryset(request):
        return Item.objects_list.action_list().order_by('-itemNum')


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
<<<<<<< HEAD

        context['progressSelect_list'] = Progress.objects.all()
        context['divisionSelect_list'] = Division.objects.all()

        context['list_type'] = 'list_filter'


=======
        context['progressSelect_list'] = Progress.objects.all()
        context['divisionSelect_list'] = Division.objects.all()

>>>>>>> origin/main
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        
     
        # 入力した検索条件の取得
        progress = self.request.GET.get('progress')
        staff = self.request.GET.get('staff')
        division = self.request.GET.get('division')
        inchargeStaff = self.request.GET.get('inchargeStaff')
        inchargeDivision = self.request.GET.get('inchargeDivision')
        word = self.request.GET.get('word')
        submissionDateFrom = self.request.GET.get('submissionDateFrom')
        submissionDateTo = self.request.GET.get('submissionDateTo')
        completionDateFrom = self.request.GET.get('completionDateFrom')
        completionDateTo = self.request.GET.get('completionDateTo')

        #  値をセッションで保持
        self.request.session['progress'] = progress
        self.request.session['staff'] = staff
        self.request.session['division'] = division
        self.request.session['inchargeStaff'] = inchargeStaff
        self.request.session['inchargeDivision'] = inchargeDivision
        self.request.session['word'] = word
        self.request.session['submissionDateFrom'] = submissionDateFrom
        self.request.session['submissionDateTo'] = submissionDateTo
        self.request.session['completionDateFrom'] = completionDateFrom
        self.request.session['completionDateTo'] = completionDateTo


        if progress =="0" and division =="0" :
            print('filter1')
            queryset = Item.objects.filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).order_by('-itemNum')

            self.request.session['item_list_type'] = 'filter1'


        elif progress =="4" and division =="0" :
            print('filter2')
            queryset = Item.objects.filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( progress__exact=4
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).filter( completionDate__range=(completionDateFrom, completionDateTo)
            ).order_by('-itemNum')

            self.request.session['item_list_type'] = 'filter2'

        
        elif progress =="4" and division !="0" :
            print('filter3')
            queryset = Item.objects.filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( progress__exact=4
            ).filter( division__exact=division
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).filter( completionDate__range=(completionDateFrom, completionDateTo)
            ).order_by('-itemNum')

            self.request.session['item_list_type'] = 'filter3'
        
        elif progress !="4" and division =="0" :
            print('filter4')
            queryset = Item.objects.filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( progress__exact=progress
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).order_by('-itemNum')

            self.request.session['item_list_type'] = 'filter4'
        
        elif progress =="0" and division !="0" :

            print('filter5')
            queryset = Item.objects.all().filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( division__exact=division
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).order_by('-itemNum')

            self.request.session['item_list_type'] = 'filter5'

        elif progress or staff or division or inchargeStaff or inchargeDivision or word or\
            (submissionDateFrom and submissionDateTo) or\
            (completionDateFrom and completionDateTo):

            print('filter6')
            queryset = Item.objects.all().filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( progress__exact=progress
            ).filter( division__exact=division
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).order_by('-itemNum')

            self.request.session['item_list_type'] = 'filter6'

        else:
            print('filter7')
            queryset = Item.objects.all().filter(deletedItem=False
            ).order_by('-itemNum')

            self.request.session['item_list_type'] = 'filter7'
        
        return queryset
   



class ItemDetail(DetailView):
    template_name = 'goodidea/detail_item.html'
    model  = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        item_list_queryset = Item.objects.all()         

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
        staff = self.request.session['staff']
        division = self.request.session['division']
        inchargeStaff = self.request.session['inchargeStaff']
        inchargeDivision = self.request.session['inchargeDivision']
        word = self.request.session['word']
        submissionDateFrom = self.request.session['submissionDateFrom']
        submissionDateTo = self.request.session['submissionDateTo']

        completionDateFrom = self.request.session['completionDateFrom']
        completionDateTo = self.request.session['completionDateTo']

<<<<<<< HEAD
  
=======

   
>>>>>>> origin/main

        if item_list_type == 'filter1':
            item_list_queryset = Item.objects.filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).order_by('-itemNum')

            print('filter_test1')

        elif item_list_type == 'filter2':
            item_list_queryset = Item.objects.filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( progress__exact=4
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).filter( completionDate__range=(completionDateFrom, completionDateTo)
            ).order_by('-itemNum') 

            print('filter_test2')


        elif item_list_type == 'filter3':
            item_list_queryset = Item.objects.filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( progress__exact=4
            ).filter( division__exact=division
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).filter( completionDate__range=(completionDateFrom, completionDateTo)
            ).order_by('-itemNum')  

            print('filter_test3')
      

        elif item_list_type == 'filter4':
            item_list_queryset =  Item.objects.filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( progress__exact=progress
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).order_by('-itemNum')    

            print('filter_test4')


        elif item_list_type == 'filter5':
            item_list_queryset = Item.objects.all().filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( division__exact=division
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).order_by('-itemNum')

            print('filter_test5')


        elif item_list_type == 'filter6':
            item_list_queryset = Item.objects.all().filter(deletedItem=False
            ).filter( submissionDate__range=(submissionDateFrom, submissionDateTo)
            ).filter( progress__exact=progress
            ).filter( division__exact=division
            ).filter( Q(staff__icontains=staff), Q(inchargeStaff__icontains=inchargeStaff),
                      Q(inchargeDivision__icontains=inchargeDivision),
                      Q(title__icontains=word)| Q(description__icontains=word)|
                      Q(discussionNote__icontains=word)| Q(report__icontains=word)
            ).order_by('-itemNum')

            print('filter_test6')


        elif item_list_type == 'filter7':
            item_list_queryset = Item.objects.all().filter(deletedItem=False
            ).order_by('-itemNum')  

            print('filter_test7')
      

        prev = item_list_queryset.filter(itemNum__lt=item.itemNum).order_by('itemNum').last()
        next = item_list_queryset.filter(itemNum__gt=item.itemNum).order_by('itemNum').first()

        context['prev'] = prev
        context['next'] = next
        return context


class ItemDetailSub(DetailView):
    template_name = 'goodidea/detail_sub.html'
    model  = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        item_list_queryset = Item.objects.item_alive()
               
        prev = item_list_queryset
        next = item_list_queryset

        context['prev'] = prev
        context['next'] = next
        return context


<<<<<<< HEAD
class ItemDetailDue(DetailView):
    template_name = 'goodidea/detail_due.html'
    model  = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        item_list_queryset = Item.objects.item_alive()
               
        prev = item_list_queryset
        next = item_list_queryset

        context['prev'] = prev
        context['next'] = next
        return context

=======
>>>>>>> origin/main

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
<<<<<<< HEAD

class ItemUpdateSub(UpdateView):
    template_name = 'goodidea/update_sub.html'
    model  = Item
    form_class = ItemUpdateFrom
    
    def get_success_url(self):
        return reverse('goodidea:detail_sub', kwargs={'pk': self.object.id})
=======
>>>>>>> origin/main
