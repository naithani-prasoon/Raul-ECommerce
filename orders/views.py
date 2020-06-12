import time
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from carts.models import Cart
from .models import Order
from .utilis import id_generator
from django.contrib.auth import get_user_model, get_user
from users.forms import UserAddressForm
from users.models import UserAddress


def orders(request):
    context = {}
    template = "users/user.html"
    return render(request, template, context)

@login_required
def checkout(request):
    User = get_user(request)

    if request.method == "POST":
        print("Hi")
        print(request.POST['stripeToken'])

    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
        print(cart)
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

    address_form = UserAddressForm()


    try:
        address_added = request.GET.get("address_added")
    except:
        address_added = None
    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None

    current_addresses= UserAddress.objects.filter(user=User)
    billing_addresses= UserAddress.objects.get_billing_addresses(user=User)
    print(billing_addresses)

    if new_order.status == "Finished":
        #cart.delete
        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse("cart"))

    context = {"address_form":address_form,
               "current_addresses": current_addresses,
               "billing_addresses": billing_addresses,
               }
    template = "Checkout.html"
    return render(request, 'orders/Checkout.html', context)
