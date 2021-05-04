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

from .models import AdminCheck, Category1, Category2, Division, DeliveryAddress, OrderRequest, OrderInfo, Payment, Progress, Supplier, StandardItem
from .forms import  CreateFormRequest, CreateFormOrder, UpdateFormRequest ,UpdateFormOrder

# Create your views here.


class ListALL(ListView):
    template_name = 'procurement/list_all.html'
    model  = OrderRequest
    fields = '__all__'
    queryset = OrderRequest.objects.filter(deletedItem=False
    ).order_by('-id').order_by('adminCheck__no')

    def get_context_data(self, **kwargs):
        context = super(ListALL, self).get_context_data(**kwargs)
        context.update({
            'object_list_order': OrderInfo.objects.all(),
        })
        return context

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

    print("test")

    def get_success_url(self):
        return reverse('procurement:detail_request', kwargs={'pk': self.object.id})


class CreateOrder(CreateView):
    template_name = 'procurement/create_order.html'
    form_class = CreateFormOrder

    def get_success_url(self):
        return reverse('procurement:detail_order', kwargs={'pk': self.object.id})



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
