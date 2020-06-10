import time
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from carts.models import Cart
from .models import Order
from .utilis import id_generator
from django.contrib.auth import get_user_model
from users.forms import UserAddressForm
from users.models import UserAddress
User = get_user_model()


def orders(request):
    context = {}
    template = "users/user.html"

    return render(request, template, context)
@login_required
def checkout(request):
    request.session.set_expiry(3)
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)

    except:
        the_id= None
        return HttpResponseRedirect(reverse("cart"))

    try:
        new_order = Order.objects.get(cart= cart)
    except Order.DoesNotExist:
        new_order = Order(cart= cart)
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
    except:
        return HttpResponseRedirect("cart")

    address_form = UserAddressForm(request.POST or None)
    if address_form.is_valid:
        new_address = address_form.save(commit=False)
        new_address.user = request.user
        new_address.save

    if new_order.status == "Finished":
        cart.delete()

        ##del  request.session['cart_id']
        ##del request.session['items_total']
        return HttpResponseRedirect(reverse("cart"))



    context = {"address_form":address_form}
    template = "Checkout.html"
    return render(request, 'orders/Checkout.html', context)