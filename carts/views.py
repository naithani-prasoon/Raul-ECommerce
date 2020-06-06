from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse


# Create your views here.

from Raul.models import product

from .models import Cart

def view(request):
    try:
        the_id = request.session['cart_id']
    except:
        the_id= None

    if the_id:
        cart = Cart.objects.get(id=the_id)
        context = {"cart": cart}
    else:
        empty_message = "Your cart is empty, go shop"
        context = {"empty" : True, "empty_message" : empty_message}

    template = "Raul/cart.html"
    return render(request, template, context)

def update_cart(request,slug):
    request.session.set_expiry(3000000)
    try:
        the_id = request.session['cart_id']
    except:
        new_cart= Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)



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


    request.session['items_total'] = cart.products.count()
    cart.total = new_total
    cart.save()

    return HttpResponseRedirect(reverse("cart"))






