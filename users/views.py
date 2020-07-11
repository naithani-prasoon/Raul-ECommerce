from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .forms import UserRegisterForm
from .forms import CreateUserForm, UserAddressForm
# from .forms import UserRegisterForm
from carts.models import Cart, CartItem
from django.contrib.auth import get_user
from django.urls import reverse
from users.models import UserAddress, UserDefaultAddress
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
    User = get_user(request)
    UserOrders = CartItem.objects.filter(user=User)
    userAddress = UserAddress.objects.filter(user=User)
    context = {"userorders":UserOrders,"userAddress":userAddress}
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
            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                default_address.shipping= new_address
                default_address.save()
            if next_page is not None:
                return HttpResponseRedirect(reverse(next_page) + "?address_added=True")







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
