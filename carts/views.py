from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse


# Create your views here.

from Raul.models import product

from .models import Cart

def view(request):
    cart = Cart.objects.all()[0]
    context = {"cart": cart}
    template = "Raul/cart.html"
    return render(request, template, context)

def update_cart(request,slug):
    cart = Cart.objects.all()[0]
    try:
        producter= product.objects.get(slug=slug)
    except product.DoesNotExist:
        pass
    except:
        pass
    if producter not in cart.products.all():
        cart.products.add(producter)
    else:
        cart.products.remove(producter)

    return HttpResponseRedirect(reverse("cart"))






