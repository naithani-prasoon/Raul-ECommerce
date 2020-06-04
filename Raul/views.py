from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import product

def home(request):
    return render(request, 'Raul/index.html')

def secondHome(request):
    return render(request, 'Raul/home.html')

def products(request):
    products= product.objects.all()
    context = {'products': products}
    template ='Raul/product.html'
    return render(request, template, context)





# Create your views here.
