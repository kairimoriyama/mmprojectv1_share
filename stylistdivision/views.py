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

from staffdb.models import StaffDB, Division
from bankaccount.models import Statement
from .models import AdminCheck, ProjectProgress, ProjectCategory, ClientCategory, Client, Settlement, Project

# Create your views here.


class ListProject(ListView):
    template_name = 'stylistdivision/list_project.html'
    model  = Project
    fields = '__all__'
    queryset = Project.objects.all()


class ListSettlement(ListView):
    template_name = 'stylistdivision/list_settlement.html'
    model  = Settlement
    fields = '__all__'
    queryset = Settlement.objects.all()

