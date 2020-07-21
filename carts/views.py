from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import CartItem, Cart
from django.contrib.auth import get_user
from Raul.models import Variation, product
from django.contrib import messages
import time
from django import http
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from users import forms
from django.contrib.auth import login,logout,authenticate

# Create your views here.

from Raul.models import product

from .models import Cart


def view(request):
    template = "Raul/cart.html"
    form = forms.LoginForms(request.POST or None)
    Register_form = forms.CreateUserForm(request.POST or None)
    context = {'form': form,"Register_form": Register_form}
    if 'register' in request.POST:
        request.session.set_expiry(60)
        if Register_form.is_valid():
            Reg = Register_form.save(commit=False)
            Reg.email = Reg.username
            Reg.save()
            Register_form = forms.CreateUserForm()
            form = forms.LoginForms()
            context = {'form': form,"Register_form": Register_form}
            messages.success(request, f'Your account has been created! You are now able to log in')
            return HttpResponseRedirect(reverse("cart"))
        else:
            messages.error(request, Register_form.error_messages)
            form = forms.LoginForms()
            context = {'form': form,"Register_form": Register_form}
            return HttpResponseRedirect(reverse("cart"))

    if 'login' in request.POST:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            context = {'form': form,"Register_form": Register_form}
            login(request,user)
            a = 4
            return HttpResponseRedirect(reverse("cart"))

    User = get_user(request)
    template = "Raul/cart.html"
    if User.is_authenticated:
        # Check is user assoicated with an ACTIVE CartID #
        try:
            cart = Cart.objects.get(id=request.session['cart_id'], active=True)
        except:
            pass
        else:
            if not cart.user and request.user.is_authenticated:
                new_total = 0.00
                for item in cart.cartitem_set.all():
                    if item.variation.all():
                        for itemV in item.variation.all():
                            if itemV.price == None:
                                print( "Product Name: ",itemV,  itemV.price)
                                new_total += float(itemV.product.price) * (item.quantity)
                                print( "New Total",  new_total)
                                line_total = float(itemV.price) * (item.quantity)
                                print("Line Total", line_total)
                                item.line_total = line_total
                            else:
                                print( "Product Name: ",itemV,  itemV.price)
                                new_total += float(itemV.price) * (item.quantity)
                                print( "New Total",  new_total)
                                line_total = float(itemV.price) * (item.quantity)
                                print("Line Total", line_total)
                                item.line_total = line_total

                        item.save()
                    else:
                        print( "Product Name: ",item,  item.product.price)
                        new_total += float(item.product.price) * (item.quantity)
                        print( "New Total",  new_total)
                        line_total = float(item.product.price) * (item.quantity)
                        print("Line Total", line_total)
                        item.line_total = line_total
                    item.save()

                request.session['items_total'] = cart.cartitem_set.count()
                cart.total = round(new_total,2)
                print(cart.total)
                cart.pennies_total = cart.total * 100
                cart.save()
                userCartNum = Cart.objects.filter(user=User, active=True).count()
                if userCartNum > 0:
                    userCart = Cart.objects.get(user=User, active=True)
                    userCart.delete()

                cart.user = User
                cart.save()
                context = {'cart': cart, 'form': form,"Register_form": Register_form}
                y = 0
                for ite in cart.cartitem_set.all():
                    y += 1
                if y == 0:
                    empty_message = "Your cart is empty, go shop"
                    context = {"empty": True, "empty_message": empty_message, 'form': form,"Register_form": Register_form}
                    return render(request, template, context)
                return render(request, template, context)

            # Check if an ACTIVE cart is asspcated with User #
        try:
            cart = Cart.objects.get(user=User, active=True)
        except:
            pass
        else:
            new_total = 0.00
            for item in cart.cartitem_set.all():
                if item.variation.all():
                    for itemV in item.variation.all():
                        if itemV.price == None:
                            print( "Product Name: ",itemV,  itemV.price)
                            new_total += float(itemV.product.price) * (item.quantity)
                            print( "New Total",  new_total)
                            line_total = float(itemV.product.price) * (item.quantity)
                            print("Line Total", line_total)
                            item.line_total = line_total
                        else:
                            print( "Product Name: ",itemV,  itemV.price)
                            new_total += float(itemV.price) * (item.quantity)
                            print( "New Total",  new_total)
                            line_total = float(itemV.price) * (item.quantity)
                            print("Line Total", line_total)
                            item.line_total = line_total

                    item.save()
                else:
                    print( "Product Name: ",item,  item.product.price)
                    new_total += float(item.product.price) * (item.quantity)
                    print( "New Total",  new_total)
                    line_total = float(item.product.price) * (item.quantity)
                    print("Line Total", line_total)
                    item.line_total = line_total
                item.save()

            request.session['items_total'] = cart.cartitem_set.count()
            cart.total = round(new_total,2)
            print(cart.total)
            cart.pennies_total = cart.total * 100
            cart.save()
            request.session['cart_id'] = cart.id
            context = {'cart': cart, 'form': form,"Register_form": Register_form}
            y = 0
            for ite in cart.cartitem_set.all():
                y += 1
            if y == 0:
                empty_message = "Your cart is empty, go shop"
                context = {"empty": True, "empty_message": empty_message, 'form': form,"Register_form": Register_form}
                return render(request, template, context)
            return render(request, template, context)




    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id, active=True)
    except:
        the_id = None

    if the_id:
        new_total = 0.00
        for item in cart.cartitem_set.all():
            if item.variation.all():
                for itemV in item.variation.all():
                    if itemV.price == None:
                        print( "Product Name: ",itemV,  itemV.price)
                        new_total += float(itemV.product.price) * (item.quantity)
                        print( "New Total",  new_total)
                        line_total = float(itemV.product.price) * (item.quantity)
                        print("Line Total", line_total)
                        item.line_total = line_total
                    else:
                        print( "Product Name: ",itemV,  itemV.price)
                        new_total += float(itemV.price) * (item.quantity)
                        print( "New Total",  new_total)
                        line_total = float(itemV.price) * (item.quantity)
                        print("Line Total", line_total)
                        item.line_total = line_total

                item.save()
            else:
                print( "Product Name: ",item,  item.product.price)
                new_total += float(item.product.price) * (item.quantity)
                print( "New Total",  new_total)
                line_total = float(item.product.price) * (item.quantity)
                print("Line Total", line_total)
                item.line_total = line_total
            item.save()

        request.session['items_total'] = cart.cartitem_set.count()
        cart.total = round(new_total,2)
        print(cart.total)
        cart.pennies_total = cart.total * 100
        cart.save()
        context = {"cart": cart, 'form': form,"Register_form": Register_form}
        y = 0
        for ite in cart.cartitem_set.all():
            y += 1
        if y == 0:
            empty_message = "Your cart is empty, go shop"
            context = {"empty": True, "empty_message": empty_message, 'form': form,"Register_form": Register_form}
            return render(request, template, context)
        return render(request, template, context)

    else:
        empty_message = "Your cart is empty, go shop"
        context = {"empty": True, "empty_message": empty_message, 'form': form,"Register_form": Register_form}
        return render(request, template, context)

    context = {"cart": cart, 'form': form,"Register_form": Register_form}
    return render(request, template, context)


def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id = the_id)
    except:
        return HttpResponseRedirect(reverse("cart"))

    cartitem = CartItem.objects.get(id=id)
    cartitem.delete()

    return HttpResponseRedirect(reverse("cart"))


def add_to_cart(request, slug):
    request.session.set_expiry(10000)
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
            new_item.quantity = int(qty)
            new_item.save()


        if Var_items2 > 1 and zero_qty == True:
            new_item.delete()
            current_item = CartItem.objects.filter(cart=cart, product=producter, variation=v)
            hi = current_item.get(variation=p)
            if int(qty) <= 0:
                hi.delete()
            else:
                hi.quantity += int(qty)
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
                    current_item.quantity += int(qty)
                    current_item.save()


    new_total = 0.00
    for item in cart.cartitem_set.all():
        if (item.quantity != None):
            new_total += float(item.product.price) * (item.quantity)
            line_total = float(item.product.price) * (item.quantity)
            item.line_total = line_total
        item.save()

    request.session['items_total'] = cart.cartitem_set.count()
    cart.total = round(new_total,2)
    cart.pennies_total = cart.total * 100
    cart.save()
    time.sleep(1.5)
    return HttpResponse('<script>history.back();</script>')


def update_cart(request, slug):
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
        if item.variation.all():
            for itemV in item.variation.all():
                if itemV.price == None:
                    print( "Product Name: ",itemV,  itemV.price)
                    new_total += float(itemV.product.price) * (item.quantity)
                    print( "New Total",  new_total)
                    line_total = float(itemV.product.price) * (item.quantity)
                    print("Line Total", line_total)
                    item.line_total = line_total
                else:
                    print( "Product Name: ",itemV,  itemV.price)
                    new_total += float(itemV.price) * (item.quantity)
                    print( "New Total",  new_total)
                    line_total = float(itemV.price) * (item.quantity)
                    print("Line Total", line_total)
                    item.line_total = line_total

            item.save()
        else:
            print( "Product Name: ",item,  item.product.price)
            new_total += float(item.product.price) * (item.quantity)
            print( "New Total",  new_total)
            line_total = float(item.product.price) * (item.quantity)
            print("Line Total", line_total)
            item.line_total = line_total
        item.save()

    request.session['items_total'] = cart.cartitem_set.count()
    cart.total = round(new_total,2)
    print(cart.total)
    cart.pennies_total = cart.total * 100
    cart.save()
    return HttpResponseRedirect(reverse("cart"))



