from decimal import Decimal
from pygeocoder import Geocoder
import stripe
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
# Create your views here.
from carts.models import Cart
from .models import Order,StripeInfo
from .utilis import id_generator,email_test,pdf,add_item
from django.contrib.auth import get_user_model, get_user
from users.forms import UserAddressForm,BillingAddressForm
from users.models import UserAddress, BillingAddress
from carts.views import add_to_cart
import pyziptax


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
  
    pyziptax.api_key = "OL9GNXzWjylg38ma"
    User = get_user(request)
    try:
        count = 0
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
        print(cart)

        for item in cart.cartitem_set.all():
            count+=1
        if count == 0:
            cart = None
            cart= Cart.objects.get(id=the_id, pennies_total=-1)
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
        final_amount = new_order.final_total
    address_form = UserAddressForm()
    billing_form = BillingAddressForm()


    try:
        address_added = request.GET.get("address_added")
    except:
        address_added = None

    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None

    try:
        address_added = request.GET.get("billing_added")
    except:
        address_added = None

    if address_added is None:
        billing_form = BillingAddressForm()
    else:
        billing_form = None



    current_addresses= UserAddress.objects.filter(user=User)
    billing_addresses2 = BillingAddress.objects.filter(user=User)





    if request.method == 'POST':
        if 'add' in request.POST:
            billing_a = request.POST["billing_address"]
            shipping_a = request.POST["shipping_address"]
            billing_address_instance = BillingAddress.objects.get(id= billing_a)
            shipping_address_instance = UserAddress.objects.get(id= shipping_a)
            # Calculate Price with Tax and Shipping
            result = Geocoder.geocode("1600 amphiteather parkway, mountain view")
            result.valid_address
            print(result)
            rate = pyziptax.get_rate(shipping_address_instance.zipcode, shipping_address_instance.city)
            two_places = Decimal(10) ** -2
            new_order.tax_total = Decimal(Decimal(rate/100) * Decimal(new_order.sub_total)).quantize(two_places)
            new_order.final_total = Decimal(new_order.sub_total) + Decimal(new_order.tax_total) + new_order.Shipping
            final_amount = new_order.final_total
            new_order.save()


            context = {
                "order":new_order,
                "billing_form": billing_form,
                "address_form": address_form,
                "shipping_selected": shipping_address_instance,
                "billing_selected":  billing_address_instance,
                "stripe_pub": stripe_pub,
                "cart" : cart
            }
            return render(request, 'orders/Checkout.html', context)



        if 'stripeToken' in request.POST:
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
                    billing_address_instance = BillingAddress.objects.get(id= billing_a)
                except:
                    billing_address_instance = None
                try:
                    shipping_address_instance = UserAddress.objects.get(id= shipping_a)
                except:
                    shipping_address_instance = None

                source = stripe.Customer.create_source(
                    user_stripe,
                    source= token
                )

                charge = stripe.Charge.create(
                    amount= int(new_order.final_total * 100),
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

                context= {
                    "billing_form": billing_form,
                    "address_form": address_form,
                    "billing_form": billing_form,
                    "cart": cart,
                    "order" : new_order,
                    "shipping_address": shipping_address_instance,
                    "billing_address": billing_address_instance
                }


                if charge["captured"]:

                    new_order.status = "Finished"
                    new_order.billing_address = billing_address_instance
                    new_order.shipping_address = shipping_address_instance
                    new_order.save()
                    email_test(context)
                    new_order.order_pdf = "Order_Number_" + new_order.order_id + ".pdf"
                    new_order.save()
                    cart.active = False
                    cart.save()
                    del request.session['cart_id']
                    del request.session["items_total"]
                    context= {
                        "billing_form": billing_form,
                        "address_form": address_form,
                        "billing_form": billing_form,
                        "cart": cart,
                        "order" : new_order,
                        "shipping_address": new_order.shipping_address,
                        "billing_address": new_order.billing_address
                    }
                    return render(request,'orders/Confirmed Order.html',context)

    context = {
        "billing_form": billing_form,
        "order":new_order,
        "address_form": address_form,
        "current_addresses": current_addresses,
        "billing_addresses": billing_addresses2,
        "stripe_pub": stripe_pub,
        "cart" : cart
    }
    return render(request, 'orders/Checkout.html', context)