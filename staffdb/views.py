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

from .models import Division, StaffDB

# Create your views here.


class ListALL(ListView):
    template_name = 'staffdb/staff_all.html'
    model  = StaffDB
    fields = '__all__'
    queryset = StaffDB.objects.all()
