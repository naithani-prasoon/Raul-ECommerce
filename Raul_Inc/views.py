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

def NYTimes(request):
    return render(request,'Raul_Inc/press-NYTimes.html')

def NYMagazine(request):
    return render(request,'Raul_Inc/press-NY-Magazine.html')

def presscoveteur(request):
    return render(request,'Raul_Inc/press-coveteur.html')

def pressmtv(request):
    return render(request,'Raul_Inc/press-mtv.html')

def presstheworldsbest(request):
    return render(request,'Raul_Inc/press-the-worlds-best-events.html')

def presswwwd(request):
    return render(request,'Raul_Inc/presswwd.html')

def pressmet(request):
    return render(request, 'Raul_Inc/press-met.html' )

def pressjet(request):
    return render(request, 'Raul_Inc/press-jet-set.html' )

def presslooktothestars(request):
    return render(request, 'Raul_Inc/press-looktothestars.html' )

def presstrendencias(request):
    return render(request, 'Raul_Inc/press-trendencias.html' )

def pressnypost(request):
    return render(request, 'Raul_Inc/press-ny-post.html')

def presspretaporter(request):
    return render(request, 'Raul_Inc/press-pretaporter.html')

def pressdaily(request):
    return render(request, 'Raul_Inc/press-dailyfrontrow.html')

def cafe(request):
    return render(request, 'Raul_Inc/cafe.html')















