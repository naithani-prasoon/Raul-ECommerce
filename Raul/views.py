from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home(request):
    return render(request,'Raul/home.html')

def about(request):
    return HttpResponse('<h1> About </h1>')




# Create your views here.
