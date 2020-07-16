from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .forms import UserRegisterForm
from .forms import CreateUserForm, UserAddressForm, BillingAddressForm
# from .forms import UserRegisterForm
from carts.models import Cart, CartItem
from django.contrib.auth import get_user
from django.urls import reverse
from users.models import UserAddress, UserDefaultAddress, BillingAddress
from django.contrib.auth import get_user_model







def register(request):
    request.session.set_expiry(3000000)
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    from orders.models import Order
    User = get_user(request)
    UserOrders = Order.objects.filter(user=User)
    print(UserOrders)
    userAddress = UserAddress.objects.filter(user=User)
    billing_address = BillingAddress.objects.filter(user=User)
    print(billing_address)
    context = {"UserOrders":UserOrders,"userAddress":userAddress, "billing_address":billing_address}
    return render(request, 'users/profile.html',context)

def add_address(request):
    try:
        next_page = request.GET.get("next")
    except:
        next_page = None
    if request.method == "POST":
        form = UserAddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            is_default= form.cleaned_data["default"]
            billing = form.cleaned_data["billing"]
            First_Name = form.cleaned_data["zipcode"]
            Last_Name = form.cleaned_data["city"]
            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                default_address.shipping= new_address
                default_address.save()
            if billing:
                billing_form = BillingAddressForm(request.POST)
                billing_form.zipcode = First_Name
                billing_form.city = Last_Name
                new_billing = billing_form.save(commit=False)
                new_billing.user = request.user
                new_billing.save()
                print(billing_form.zipcode)
            if next_page is not None:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_billing_address(request):
    try:
        next_page = request.GET.get("next")
    except:
        next_page = None
    if request.method == "POST":
        form = BillingAddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            is_default= form.cleaned_data["default"]
            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                default_address.billing= new_address
                default_address.save()
            if next_page is not None:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def delete_address(request, id):
    address = UserAddress.objects.get(id=id)
    address.delete()
    return HttpResponseRedirect(reverse("profile"))

# def search(request):
#     try:
#         q= request.GET.get('q')
#     except:
#         q= None
#     if q:
#         products= products.objects.filter(title__icontains=q)
#         context = {'query':q , 'products':products}
#         template = 'Raul/results.html'
#     else:
#         context = {}
#         template ='Raul/product.html'
#     return render(request, template, context)

# Create your views here.
