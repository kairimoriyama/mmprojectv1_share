from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

# Create your views here.

    
class ItemIndex(TemplateView):
    template_name = 'receipt/index.html'