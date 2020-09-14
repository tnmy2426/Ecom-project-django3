from django.shortcuts import render, HttpResponse

# importing class based views
from django.views.generic import DetailView, ListView

#models
from .models import Product, Category

#Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Home(ListView):
    paginate_by = 4
    model = Product
    template_name='App_Shop/home_page.html'


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name='App_Shop/product_details_page.html'
