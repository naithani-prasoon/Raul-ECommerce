from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home(request):
    return render(request, 'Raul/index.html')

def secondHome(request):
    return render(request, 'Raul/home.html')




# Create your views here.
