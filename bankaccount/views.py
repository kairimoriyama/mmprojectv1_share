from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView


# Create your views here.


class StatementList(ListView):
    template_name = 'bankaccount/list_all.html'
    fields = '__all__'
    paginate_by = 22

