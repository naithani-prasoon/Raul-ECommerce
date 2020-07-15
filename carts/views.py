from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import CartItem, Cart
from django.contrib.auth import get_user
from Raul.models import Variation, product
from django.contrib import messages
import time

# Create your views here.

from Raul.models import product

from .models import Cart


def view(request):
    User = get_user(request)
    template = "Raul/cart.html"
    if User.is_authenticated:
        # Check is user assoicated with an ACTIVE CartID #
        try:
            cart = Cart.objects.get(id=request.session['cart_id'], active=True)
            print("Try with ID")
        except:
            pass
        else:
            print("cart.user and request.user.is_authenticated:")
            if not cart.user and request.user.is_authenticated:
                new_total = 0.00
                for item in cart.cartitem_set.all():
                    if (item.quantity != None):
                        # print(item.product)
                        new_total += float(item.product.price) * (item.quantity)
                        line_total = float(item.product.price) * (item.quantity)
                        item.line_total = line_total
                        # print(item.line_total)
                    item.save()

                request.session['items_total'] = cart.cartitem_set.count()
                cart.total = new_total
                cart.pennies_total = cart.total * 100
                cart.save()
                userCartNum = Cart.objects.filter(user=User, active=True).count()
                if userCartNum > 0:
                    userCart = Cart.objects.get(user=User, active=True)
                    userCart.delete()

                cart.user = User
                cart.save()
                context = {'cart': cart}
                return render(request, template, context)

            # Check if an ACTIVE cart is asspcated with User #
        try:
            cart = Cart.objects.get(user=User, active=True)
        except:
            pass
        else:
            new_total = 0.00
            for item in cart.cartitem_set.all():
                if (item.quantity != None):
                    # print(item.product)
                    new_total += float(item.product.price) * (item.quantity)
                    line_total = float(item.product.price) * (item.quantity)
                    item.line_total = line_total
                    # print(item.line_total)
                item.save()

            request.session['items_total'] = cart.cartitem_set.count()
            cart.total = new_total
            cart.pennies_total = cart.total * 100
            cart.save()
            request.session['cart_id'] = cart.id
            context = {'cart': cart}
            return render(request, template, context)

    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id, active=True)
    except:
        the_id = None

    if the_id:
        new_total = 0.00
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * item.quantity
            new_total += line_total
        request.session['items_total'] = cart.cartitem_set.count()
        cart.total = new_total
        cart.save()
        context = {"cart": cart}
        return render(request, template, context)

    else:
        empty_message = "Your cart is empty, go shop"
        context = {"empty": True, "empty_message": empty_message}
        return render(request, template, context)

    context = {"cart": cart}
    return render(request, template, context)


def remove_from_cart(request, id):
    print("yooooo")
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id = the_id)
    except:
        return HttpResponseRedirect(reverse("cart"))

    cartitem = CartItem.objects.get(id=id)
    cartitem.delete()
    return HttpResponseRedirect(reverse("cart"))


def add_to_cart(request, slug):
    print("add_to_cart")
    request.session.set_expiry(3000000)
    Check = False
    Zero_Check = False
    Var_items = 0
    Var_items2 = 0
    single_item = 0
    zero_qty = True

    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)

    try:
        producter = product.objects.get(slug=slug)
    except product.DoesNotExist:
        pass
    except:
        pass

    pro_var = []
    if request.method == "POST":
        count = 0
        print("FORM POST")
        print(request.POST)
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                if count == 0:
                    v = Variation.objects.get(product=producter, category__iexact=key, title__iexact=val)
                    pro_var.append(v)
                    Var_items = CartItem.objects.filter(cart=cart, product=producter, variation=v)
                    count +=1

                if count == 1:
                    p = Variation.objects.get(product=producter, category__iexact=key, title__iexact=val)
                    pro_var.append(p)
                    Var_items = CartItem.objects.filter(cart=cart, product=producter, variation=v)
                    Var_items2 = Var_items.filter(variation=p).count()

            except:
                pass

        new_item = CartItem.objects.create(cart=cart, product=producter)
        single_item = CartItem.objects.filter(cart=cart, product=producter).count()



        if len(pro_var) > 0 and zero_qty == True:
            for item in pro_var:
                new_item.variation.add(item)
            Var_items = CartItem.objects.filter(cart=cart, product=producter, variation=v)
            Var_items2 = Var_items.filter(variation=p).count()
            Check = True


        if int(qty) <= 0 and single_item == 1:
            new_item.delete()
        elif int(qty) <= 0 and (Var_items == 1 or Var_items2 == 1):
            new_item.delete()
        else:
            new_item.quantity = qty
            new_item.save()


        if Var_items2 > 1 and zero_qty == True:
            new_item.delete()
            current_item = CartItem.objects.filter(cart=cart, product=producter, variation=v)
            hi = current_item.get(variation=p)
            if int(qty) <= 0:
                hi.delete()
            else:
                hi.quantity = int(qty)
                hi.save()
            Var_items = 0
            Check = True


        if not Check:
            if single_item > 1:
                new_item.delete()
                current_item = CartItem.objects.get(cart=cart, product=producter)
                if int(qty) <= 0:
                    current_item.delete()
                else:
                    current_item.quantity = int(qty)
                    current_item.save()


    new_total = 0.00
    for item in cart.cartitem_set.all():
        if (item.quantity != None):
            # print(item.product)
            new_total += float(item.product.price) * (item.quantity)
            line_total = float(item.product.price) * (item.quantity)
            item.line_total = line_total
            # print(item.line_total)
        item.save()

    request.session['items_total'] = cart.cartitem_set.count()
    cart.total = round(new_total,2)
    cart.pennies_total = cart.total * 100
    cart.save()
    time.sleep(1.5)
    return HttpResponse('<script>history.back();</script>')


def update_cart(request, slug):
    print("Update")
    request.session.set_expiry(3000000)
    Check = False
    Zero_Check = False
    Var_items = 0
    Var_items2 = 0
    single_item = 0
    zero_qty = True

    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)

    try:
        producter = product.objects.get(slug=slug)
    except product.DoesNotExist:
        pass
    except:
        pass

    pro_var = []
    if request.method == "POST":
        count = 0
        print("FORM POST")
        print(request.POST)
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                if count == 0:
                    v = Variation.objects.get(product=producter, category__iexact=key, title__iexact=val)
                    pro_var.append(v)
                    Var_items = CartItem.objects.filter(cart=cart, product=producter, variation=v)
                    count +=1

                if count == 1:
                    p = Variation.objects.get(product=producter, category__iexact=key, title__iexact=val)
                    pro_var.append(p)
                    Var_items = CartItem.objects.filter(cart=cart, product=producter, variation=v)
                    Var_items2 = Var_items.filter(variation=p).count()

            except:
                pass

        new_item = CartItem.objects.create(cart=cart, product=producter)
        single_item = CartItem.objects.filter(cart=cart, product=producter).count()



        if len(pro_var) > 0 and zero_qty == True:
            for item in pro_var:
                new_item.variation.add(item)
            Var_items = CartItem.objects.filter(cart=cart, product=producter, variation=v)
            Var_items2 = Var_items.filter(variation=p).count()
            Check = True


        if int(qty) <= 0 and single_item == 1:
            new_item.delete()
        elif int(qty) <= 0 and (Var_items == 1 or Var_items2 == 1):
            new_item.delete()
        else:
            new_item.quantity = qty
            new_item.save()


        if Var_items2 > 1 and zero_qty == True:
            new_item.delete()
            current_item = CartItem.objects.filter(cart=cart, product=producter, variation=v)
            hi = current_item.get(variation=p)
            if int(qty) <= 0:
                hi.delete()
            else:
                hi.quantity = int(qty)
                hi.save()
            Var_items = 0
            Check = True


        if not Check:
            if single_item > 1:
                new_item.delete()
                current_item = CartItem.objects.get(cart=cart, product=producter)
                if int(qty) <= 0:
                    current_item.delete()
                else:
                    current_item.quantity = int(qty)
                    current_item.save()


    new_total = 0.00
    for item in cart.cartitem_set.all():
        if (item.quantity != None):
            # print(item.product)
            new_total += float(item.product.price) * (item.quantity)
            line_total = float(item.product.price) * (item.quantity)
            item.line_total = line_total
            # print(item.line_total)
        item.save()

    request.session['items_total'] = cart.cartitem_set.count()
    cart.total = round(new_total,2)
    cart.pennies_total = cart.total * 100
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



