from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import CartItem, Cart


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

    cart_item, created = CartItem.objects.get_or_create(product=producter)
    if created:
        print("Yes")
    if cart_item not in cart.items.all():
        cart.items.add(cart_item)
    else:
        cart.items.remove(cart_item)

    new_total = 0.00
    for item in cart.items.all():
        new_total += float(item.product.price)

    request.session['items_total'] = cart.items.count()
    cart.total = new_total
    cart.save()
    return redirect(reverse("cart"))






