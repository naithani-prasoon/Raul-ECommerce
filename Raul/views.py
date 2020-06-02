from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home(request):
    return render(request, 'Raul/index.html')

def about(request):
    return render(request, 'Raul/about.html')




# Create your views here.
