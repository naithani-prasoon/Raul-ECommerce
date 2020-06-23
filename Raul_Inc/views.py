from django.shortcuts import render

# Create your views here.

def home(request):
    context= {}
    return render(request, 'Raul_Inc/home.html',context)

