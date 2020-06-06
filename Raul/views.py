from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import product, Category


def home(request):
    return render(request, 'Raul/index.html')


def secondHome(request):
    return render(request, 'Raul/home.html')


def landingpage(request):
    return render(request, 'Raul/landing.html')


def products(request):
    products = product.objects.all()
    context = {'products': products}
    template = 'Raul/product.html'
    return render(request, template, context)


def CategoryView(request, cats):
    cat_products = product.objects.filter(category=cats)
    return render(request, 'Raul/categories.html', {'cats': cats, 'cat_products': cat_products})


def singleView(request, slug):
    try:
        single_product = product.objects.get(slug=slug)
        context = {'single_product': single_product}
        return render(request, 'Raul/single_product.html', context)
    except:
        raise

# Create your views here.
