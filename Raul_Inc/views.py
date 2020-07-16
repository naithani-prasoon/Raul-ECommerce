from django.shortcuts import render

# Create your views here.

def home(request):
    context= {}
    return render(request, 'Raul_Inc/home.html',context)

def bio(request):
    return render(request,'Raul_Inc/bio.html')

def press(request):
    return render(request,'Raul_Inc/press.html')

def clientList(request):
    return render(request,'Raul_Inc/clientList.html')

def contact(request):
    return render(request,'Raul_Inc/contact.html')



