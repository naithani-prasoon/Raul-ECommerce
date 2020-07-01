import time

import stripe
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
# Create your views here.
from carts.models import Cart
from .models import Order
from .utilis import id_generator,email_test,make_invoice
from django.contrib.auth import get_user_model, get_user
from users.forms import UserAddressForm
from users.models import UserAddress
from carts.views import add_to_cart
header = ['product','quantity','line_total']
arr = []
arr.append(header)

try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret = settings.STRIPE_SECRET_KEY

except Exception as e:
    print(str(e))
    raise NotImplementedError(str(e))

stripe.api_key = stripe_secret

def orders(request):
    context = {}
    template = "users/user.html"
    return render(request, template, context)

@login_required
def checkout(request):
    User = get_user(request)
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
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.sub_total = cart.total
        new_order.save()
    except:
        new_order = None
        return HttpResponseRedirect("cart")

    final_amount = 0.00
    if new_order is not None:
        new_order.sub_total = cart.total
        new_order.save()
        final_amount = new_order.get_final_amount()

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


    if request.method == "POST":
        #print("hi" + request.POST['stripeToken'])
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
        except:
            customer = None

        if customer is not None:
            print(request.POST)
            billing_a = request.POST["billing_address"]
            shipping_a = request.POST["shipping_address"]

            token = request.POST['stripeToken']
            try:
                billing_address_instance = UserAddress.objects.get(id= billing_a)
            except:
                billing_address_instance = None
            try:
                shipping_address_instance = UserAddress.objects.get(id= shipping_a)
            except:
                shipping_address_instance = None
            print(billing_a)
            print(shipping_address_instance)


            source = stripe.Customer.create_source(
                user_stripe,
                source= token
            )
            charge = stripe.Charge.create(
                amount= int(final_amount * 100),
                currency="usd",
                source = source,
                customer = customer,
                description = "Test"
            )
            add_stripe_info = stripe.Customer.modify_source(
                customer.id,
                source.id,
                address_city = billing_address_instance.city,
                address_country = billing_address_instance.country,
                address_line1 = billing_address_instance.address,
                address_zip = billing_address_instance.zipcode,
                address_state = billing_address_instance.state,
            )

            if charge["captured"]:
                new_order.status = "Finished"
                new_order.billing_address = billing_address_instance
                new_order.shipping_address = shipping_address_instance
                new_order.save()
                for i in cart.cartitem_set.all():
                    order = [i.product, i.quantity, i.line_total]
                    arr.append(order)
                make_invoice(arr,new_order.order_id)
                new_order.order_pdf = "Order_Number_" + new_order.order_id + ".pdf"
                new_order.save()
                email_test()
                cart.active = False
                cart.save()
                del request.session['cart_id']
                return render(request,'orders/Confirmed Order.html')

    context = {
                "order":new_order,
                "address_form": address_form,
                "current_addresses": current_addresses,
                "billing_addresses": billing_addresses,
                "stripe_pub": stripe_pub,
               }
    template = "Checkout.html"
    return render(request, 'orders/Checkout.html', context)
