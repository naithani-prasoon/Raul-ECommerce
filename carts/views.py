from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import CartItem,Cart
from django.contrib.auth import get_user
from Raul.models import Variation, product



# Create your views here.

from Raul.models import product

from .models import Cart

def view(request):
    User = get_user(request)
    template = "Raul/cart.html"
    if User.is_authenticated:
        # Check is user assoicated with an ACTIVE CartID #
        try:
            cart = Cart.objects.get(id=request.session['cart_id'],active=True)
            print("Try with ID")
        except :
            pass
        else:
            print("cart.user and request.user.is_authenticated:")
            if not cart.user and request.user.is_authenticated:
                userCartNum = Cart.objects.filter(user=User,active=True).count()
                if userCartNum > 0:
                    userCart = Cart.objects.get(user=User,active=True)
                    userCart.delete()

                cart.user = User
                cart.save()
                context = {'cart': cart}
                return render(request, template, context)

            # Check if an ACTIVE cart is asspcated with User #
        try:
            cart = Cart.objects.get(user=User,active=True)
        except:
            pass
        else:
            request.session['cart_id'] = cart.id
            context= {'cart':cart}
            return render(request, template, context)


    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id,active=True)
    except:
        the_id= None

    if the_id:
        new_total = 0.00
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * item.quantity
            new_total += line_total
        request.session['items_total'] = cart.cartitem_set.count()
        cart.total = new_total
        cart.save()
        context = {"cart":cart}
        return render(request, template, context)

    else:
        empty_message = "Your cart is empty, go shop"
        context = {"empty" : True, "empty_message" : empty_message}
        return render(request, template, context)

    context = {"cart":cart}
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

    pro_var = []
    if request.method == "POST":
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                v = Variation.objects.get(product=producter, category__iexact= key, title__iexact=val)
                pro_var.append(v)
            except:
                pass



        cart_item, created = CartItem.objects.get_or_create(cart= cart, product=producter)

        if request.user.is_authenticated:
            print("hi")
            cart.user = request.user
            cart_item.user = request.user


        if int(qty) <= 0:
            cart_item.delete()
        else:
            if len(pro_var) > 0:
                cart_item.variation.clear()
                for item in pro_var:
                    cart_item.variation.add(item)
            cart_item.quantity = qty
            cart_item.save()



    new_total = 0.00
    for item in cart.cartitem_set.all():
        if(item.quantity != None):
            print(item.product)
            new_total += float(item.product.price) * (item.quantity)
            line_total = float(item.product.price) * (item.quantity)
            item.line_total = line_total
            print(item.line_total)
        item.save()

    request.session['items_total'] = cart.cartitem_set.count()
    cart.total = new_total
    cart.pennies_total = cart.total * 100
    cart.save()

    return redirect(reverse("cart"))










