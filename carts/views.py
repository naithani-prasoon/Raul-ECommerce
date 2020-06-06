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

    new_total = 0.00
    for item in cart.products.all():
        new_total += float(item.price)

    cart.total = new_total
    cart.save()

    return HttpResponseRedirect(reverse("cart"))






