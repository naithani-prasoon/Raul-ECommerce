import time
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from carts.models import Cart
from .models import Order
from .utilis import id_generator
def orders(request):
    context = {}
    template = "users/user.html"
    return render(request, template, context)

def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
        print(cart)
    except:
        the_id= None
        return HttpResponseRedirect(reverse("cart"))

    new_order, created = Order.objects.get_or_create(cart=cart)
    if created:
        #user
        #address
        #cc
        new_order.order_id = id_generator()
        new_order.save()
    new_order.user = request.user
    new_order.save()
    if new_order.status == "Finished":
        #cart.delete
        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse("cart"))

    context = {}
    template = "Raul/product.html"
    return render(request, template, context)