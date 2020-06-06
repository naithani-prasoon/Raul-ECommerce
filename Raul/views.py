from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import product, Category


def search(request):
    try:
        q= request.GET.get('q')
    except:
        q= None
    if q:
        products= product.objects.filter(title__icontains=q)
        pro=product.price
        context = {'query': q , 'products': products, "price" : pro}
        template = 'Raul/results.html'
    else:
        context = {}
        template ='Raul/product.html'
    return render(request, template, context)



def home(request):
    return render(request, 'Raul/index.html')

def secondHome(request):
    return render(request, 'Raul/home.html')

def landingpage(request):
    return render(request, 'Raul/landing.html')

def products(request):
    products= product.objects.all()
    context = {'products': products}
    template ='Raul/product.html'
    return render(request, template, context)

def CategoryView(request, cats):
    cat_products = product.objects.filter(category=cats)
    for i in cat_products:
        print(i)
    return render(request,'Raul/categories.html', {'cats': cats,'cat_products':cat_products})










# Create your views here.
