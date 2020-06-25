from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import product, Category
from users import forms
from django.contrib.auth import login,logout,authenticate


def search(request):
    try:
        q= request.GET.get('q')
    except:
        q= None
    if q:
        products1= product.objects.filter(title__icontains=q)
        pro= product.price
        context = {'query': q , 'products1': products1, "price" : pro}
        template = 'Raul/results.html'
    else:
        context = {}
        template = 'Raul/product.html'
    return render(request, template, context)


def home(request):
    return render(request, 'Raul_Inc/index.html')


def secondHome(request):
    form = forms.LoginForms(request.POST or None)
    RegisterForm = forms.CreateUserForm(request.POST or None)
    context = {'form': form,"Register_form": RegisterForm}
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username,password=password)
        login(request,user)
    return render(request, 'Raul/home.html',context)


def landingpage(request):
    return render(request, 'Raul/landing.html')


def products(request):
    products = product.objects.all()
    context = {'products': products}
    template = 'Raul/product.html'
    return render(request, template, context)


def CategoryView(request, cats):
    cat_products = product.objects.filter(category=cats)
    banner = Category.objects.get(name=cats)
    for i in cat_products:
        print(i.title)
    return render(request, 'Raul/categories.html', {'cats': cats, 'cat_products': cat_products,'banner':banner})


def SectionView(request,cats):
    print(cats)
    cat_products = product.objects.filter(section__iexact=cats)

    for i in cat_products:
        print(i.title)
    return render(request, 'Raul/categories.html', {'cats': cats, 'cat_products': cat_products})



def singleView(request, slug):
    try:
        single_product = product.objects.get(slug=slug)
        context = {'single_product': single_product}
        return render(request, 'Raul/single_product.html', context)
    except:
        raise


# Create your views here.
