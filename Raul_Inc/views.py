from django.shortcuts import render
from Raul_Inc import templates

# Create your views here.
def home(request):
    return render(request,'Raul_Inc/home.html')